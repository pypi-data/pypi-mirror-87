# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2020 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Customer Order Views
"""

from __future__ import unicode_literals, absolute_import

import six
from sqlalchemy import orm

from rattail.db import model

from webhelpers2.html import tags

from tailbone.db import Session
from tailbone.views import MasterView


class CustomerOrdersView(MasterView):
    """
    Master view for customer orders
    """
    model_class = model.CustomerOrder
    route_prefix = 'custorders'
    editable = False
    deletable = False

    grid_columns = [
        'id',
        'customer',
        'person',
        'created',
        'status_code',
    ]

    form_fields = [
        'id',
        'customer',
        'person',
        'phone_number',
        'email_address',
        'created',
        'status_code',
    ]

    def query(self, session):
        return session.query(model.CustomerOrder)\
                      .options(orm.joinedload(model.CustomerOrder.customer))

    def configure_grid(self, g):
        super(CustomerOrdersView, self).configure_grid(g)

        g.set_joiner('customer', lambda q: q.outerjoin(model.Customer))
        g.set_joiner('person', lambda q: q.outerjoin(model.Person))

        g.filters['customer'] = g.make_filter('customer', model.Customer.name,
                                              label="Customer Name",
                                              default_active=True,
                                              default_verb='contains')
        g.filters['person'] = g.make_filter('person', model.Person.display_name,
                                            label="Person Name",
                                            default_active=True,
                                            default_verb='contains')

        g.set_sorter('customer', model.Customer.name)
        g.set_sorter('person', model.Person.display_name)

        g.set_sort_defaults('created', 'desc')

        # TODO: enum choices renderer
        g.set_label('status_code', "Status")
        g.set_label('id', "ID")

    def configure_form(self, f):
        super(CustomerOrdersView, self).configure_form(f)

        # id
        f.set_readonly('id')
        f.set_label('id', "ID")

        # person
        f.set_renderer('person', self.render_person)

        # created
        f.set_readonly('created')

        # label overrides
        f.set_label('status_code', "Status")

    def render_person(self, order, field):
        person = order.person
        if not person:
            return ""
        text = six.text_type(person)
        url = self.request.route_url('people.view', uuid=person.uuid)
        return tags.link_to(text, url)

    def create(self, form=None, template='create'):
        """
        View for creating a new customer order.  Note that it does so by way of
        maintaining a "new customer order" batch, until the user finally
        submits the order, at which point the batch is converted to a proper
        order.
        """
        batch = self.get_current_batch()

        if self.request.method == 'POST':

            # first we check for traditional form post
            action = self.request.POST.get('action')
            post_actions = [
                'start_over_entirely',
                'delete_batch',
            ]
            if action in post_actions:
                return getattr(self, action)(batch)

            # okay then, we'll assume newer JSON-style post params
            data = dict(self.request.json_body)
            action = data.get('action')
            json_actions = [
                'get_customer_info',
                'set_customer_data',
                'submit_new_order',
            ]
            if action in json_actions:
                result = getattr(self, action)(batch, data)
                return self.json_response(result)

        context = {'batch': batch}
        return self.render_to_response(template, context)

    def get_current_batch(self):
        user = self.request.user
        if not user:
            raise RuntimeError("this feature requires a user to be logged in")

        try:
            # there should be at most *one* new batch per user
            batch = self.Session.query(model.CustomerOrderBatch)\
                                .filter(model.CustomerOrderBatch.mode == self.enum.CUSTORDER_BATCH_MODE_CREATING)\
                                .filter(model.CustomerOrderBatch.created_by == user)\
                                .one()

        except orm.exc.NoResultFound:
            # no batch yet for this user, so make one
            batch = model.CustomerOrderBatch()
            batch.mode = self.enum.CUSTORDER_BATCH_MODE_CREATING
            batch.created_by = user
            self.Session.add(batch)
            self.Session.flush()

        return batch

    def start_over_entirely(self, batch):
        # just delete current batch outright
        # TODO: should use self.handler.do_delete() instead?
        self.Session.delete(batch)
        self.Session.flush()

        # send user back to normal "create" page; a new batch will be generated
        # for them automatically
        route_prefix = self.get_route_prefix()
        url = self.request.route_url('{}.create'.format(route_prefix))
        return self.redirect(url)

    def delete_batch(self, batch):
        # just delete current batch outright
        # TODO: should use self.handler.do_delete() instead?
        self.Session.delete(batch)
        self.Session.flush()

        # set flash msg just to be more obvious
        self.request.session.flash("New customer order has been deleted.")

        # send user back to customer orders page, w/ no new batch generated
        route_prefix = self.get_route_prefix()
        url = self.request.route_url(route_prefix)
        return self.redirect(url)

    def get_customer_info(self, batch, data):
        uuid = data.get('uuid')
        if not uuid:
            return {'error': "Must specify a customer UUID"}

        customer = self.Session.query(model.Customer).get(uuid)
        if not customer:
            return {'error': "Customer not found"}

        return self.info_for_customer(batch, data, customer)

    def info_for_customer(self, batch, data, customer):
        phone = customer.first_phone()
        email = customer.first_email()
        return {
            'uuid': customer.uuid,
            'phone_number': phone.number if phone else None,
            'email_address': email.address if email else None,
        }

    def set_customer_data(self, batch, data):
        if 'customer_uuid' in data:
            batch.customer_uuid = data['customer_uuid']
            if 'person_uuid' in data:
                batch.person_uuid = data['person_uuid']
            elif batch.customer_uuid:
                self.Session.flush()
                batch.person = batch.customer.first_person()
            else: # no customer set
                batch.person_uuid = None
        if 'phone_number' in data:
            batch.phone_number = data['phone_number']
        if 'email_address' in data:
            batch.email_address = data['email_address']
        self.Session.flush()
        return {'success': True}

    def submit_new_order(self, batch, data):
        # TODO
        return {'success': True}


def includeme(config):
    CustomerOrdersView.defaults(config)

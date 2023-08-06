## -*- coding: utf-8; -*-
<%inherit file="/master/create.mako" />

<%def name="extra_styles()">
  ${parent.extra_styles()}
  % if use_buefy:
      <style type="text/css">
        .this-page-content {
            flex-grow: 1;
        }
      </style>
  % endif
</%def>

<%def name="page_content()">
  <br />
  % if use_buefy:
      <customer-order-creator></customer-order-creator>
  % else:
      <p>Sorry, but this page is not supported by your current theme configuration.</p>
  % endif
</%def>

<%def name="order_form_buttons()">
  <div class="buttons">
    <b-button type="is-primary"
              @click="submitOrder()"
              icon-pack="fas"
              icon-left="fas fa-upload">
      Submit this Order
    </b-button>
    <b-button @click="startOverEntirely()"
              icon-pack="fas"
              icon-left="fas fa-redo">
      Start Over Entirely
    </b-button>
    <b-button @click="cancelOrder()"
              type="is-danger"
              icon-pack="fas"
              icon-left="fas fa-trash">
      Cancel this Order
    </b-button>
  </div>
</%def>

<%def name="render_this_page_template()">
  ${parent.render_this_page_template()}

  <script type="text/x-template" id="customer-order-creator-template">
    <div>

      ${self.order_form_buttons()}

      <b-collapse class="panel" :class="customerPanelType"
                  :open.sync="customerPanelOpen">

        <div slot="trigger"
             slot-scope="props"
             class="panel-heading"
             role="button">
          <b-icon pack="fas"
            ## TODO: this icon toggling should work, according to
            ## Buefy docs, but i could not ever get it to work.
            ## what am i missing?
            ## https://buefy.org/documentation/collapse/
            ## :icon="props.open ? 'caret-down' : 'caret-right'">
            ## (for now we just always show caret-right instead)
            icon="caret-right">
          </b-icon>
          <strong v-html="customerPanelHeader"></strong>
        </div>

        <div class="panel-block">
          <div style="width: 100%;">

            <div style="display: flex; flex-direction: row;">
              <div style="flex-grow: 1; margin-right: 1rem;">
                <b-notification :type="customerStatusType"
                                position="is-bottom-right"
                                :closable="false">
                  {{ customerStatusText }}
                </b-notification>
              </div>
              <!-- <div class="buttons"> -->
              <!--   <b-button @click="startOverCustomer()" -->
              <!--             icon-pack="fas" -->
              <!--             icon-left="fas fa-redo"> -->
              <!--     Start Over -->
              <!--   </b-button> -->
              <!-- </div> -->
            </div>

            <br />
            <div class="field">
              <b-radio v-model="customerIsKnown"
                       :native-value="true">
                Customer is already in the system.
              </b-radio>
            </div>

            <div v-show="customerIsKnown">
              <b-field label="Customer Name" horizontal>
                <tailbone-autocomplete
                   ref="customerAutocomplete"
                   v-model="customerUUID"
                   :initial-label="customerDisplay"
                   serviceUrl="${url('customers.autocomplete')}"
                   @input="customerChanged">
                </tailbone-autocomplete>
              </b-field>
              <b-field label="Phone Number" horizontal>
                <b-input v-model="phoneNumberEntry"
                         @input="phoneNumberChanged"
                         @keydown.native="phoneNumberKeyDown">
                </b-input>
                <b-button v-if="!phoneNumberSaved"
                          type="is-primary"
                          icon-pack="fas"
                          icon-left="fas fa-save"
                          @click="setCustomerData()">
                  Please save when finished editing
                </b-button>
                <!-- <tailbone-autocomplete -->
                <!--    serviceUrl="${url('customers.autocomplete.phone')}"> -->
                <!-- </tailbone-autocomplete> -->
              </b-field>
            </div>

            <br />
            <div class="field">
              <b-radio v-model="customerIsKnown" disabled
                       :native-value="false">
                Customer is not yet in the system.
              </b-radio>
            </div>

            <div v-if="!customerIsKnown">
              <b-field label="Customer Name" horizontal>
                <b-input v-model="customerName"></b-input>
              </b-field>
              <b-field label="Phone Number" horizontal>
                <b-input v-model="phoneNumber"></b-input>
              </b-field>
            </div>

          </div>
        </div> <!-- panel-block -->
      </b-collapse>

      <b-collapse class="panel"
                  open>

        <div slot="trigger"
             slot-scope="props"
             class="panel-heading"
             role="button">
          <b-icon pack="fas"
            ## TODO: this icon toggling should work, according to
            ## Buefy docs, but i could not ever get it to work.
            ## what am i missing?
            ## https://buefy.org/documentation/collapse/
            ## :icon="props.open ? 'caret-down' : 'caret-right'">
            ## (for now we just always show caret-right instead)
            icon="caret-right">
          </b-icon>
          <strong>Items</strong>
        </div>

        <div class="panel-block">
          <div>
            TODO: items go here
          </div>
        </div>
      </b-collapse>

      ${self.order_form_buttons()}

      ${h.form(request.current_route_url(), ref='batchActionForm')}
      ${h.csrf_token(request)}
      ${h.hidden('action', **{'v-model': 'batchAction'})}
      ${h.end_form()}

    </div>
  </script>
</%def>

<%def name="make_this_page_component()">
  ${parent.make_this_page_component()}
  <script type="text/javascript">

    const CustomerOrderCreator = {
        template: '#customer-order-creator-template',
        data() {
            return {
                batchAction: null,

                customerPanelOpen: true,
                customerIsKnown: true,
                customerUUID: ${json.dumps(batch.customer_uuid)|n},
                customerDisplay: ${json.dumps(six.text_type(batch.customer or ''))|n},
                customerEntry: null,
                phoneNumberEntry: ${json.dumps(batch.phone_number)|n},
                phoneNumberSaved: true,
                customerName: null,
                phoneNumber: null,

                ## TODO: should find a better way to handle CSRF token
                csrftoken: ${json.dumps(request.session.get_csrf_token() or request.session.new_csrf_token())|n},
            }
        },
        computed: {
            customerPanelHeader() {
                let text = "Customer"

                if (this.customerIsKnown) {
                    if (this.customerUUID) {
                        if (this.$refs.customerAutocomplete) {
                            text = "Customer: " + this.$refs.customerAutocomplete.getDisplayText()
                        } else {
                            text = "Customer: " + this.customerDisplay
                        }
                    }
                } else {
                    if (this.customerName) {
                        text = "Customer: " + this.customerName
                    }
                }

                if (!this.customerPanelOpen) {
                    text += ' <p class="' + this.customerHeaderClass + '" style="display: inline-block; float: right;">' + this.customerStatusText + '</p>'
                }

                return text
            },
            customerHeaderClass() {
                if (!this.customerPanelOpen) {
                    if (this.customerStatusType == 'is-danger') {
                        return 'has-text-danger'
                    } else if (this.customerStatusType == 'is-warning') {
                        return 'has-text-warning'
                    }
                }
            },
            customerPanelType() {
                if (!this.customerPanelOpen) {
                    return this.customerStatusType
                }
            },
            customerStatusType() {
                return this.customerStatusTypeAndText.type
            },
            customerStatusText() {
                return this.customerStatusTypeAndText.text
            },
            customerStatusTypeAndText() {
                let phoneNumber = null
                if (this.customerIsKnown) {
                    if (!this.customerUUID) {
                        return {
                            type: 'is-danger',
                            text: "Please identify the customer.",
                        }
                    }
                    if (!this.phoneNumberEntry) {
                        return {
                            type: 'is-warning',
                            text: "Please provide a phone number for the customer.",
                        }
                    }
                    phoneNumber = this.phoneNumberEntry
                } else { // customer is not known
                    if (!this.customerName) {
                        return {
                            type: 'is-danger',
                            text: "Please identify the customer.",
                        }
                    }
                    if (!this.phoneNumber) {
                        return {
                            type: 'is-warning',
                            text: "Please provide a phone number for the customer.",
                        }
                    }
                    phoneNumber = this.phoneNumber
                }

                let phoneDigits = phoneNumber.replace(/\D/g, '')
                if (!phoneDigits.length || (phoneDigits.length != 7 && phoneDigits.length != 10)) {
                    return {
                        type: 'is-warning',
                        text: "The phone number does not appear to be valid.",
                    }
                }

                if (!this.customerIsKnown) {
                    return {
                        type: 'is-warning',
                        text: "Will create a new customer record.",
                    }
                }

                return {
                    type: null,
                    text: "Everything seems to be okay here.",
                }
            },
        },
        methods: {

            startOverEntirely() {
                let msg = "Are you sure you want to start over entirely?\n\n"
                    + "This will totally delete this order and start a new one."
                if (!confirm(msg)) {
                    return
                }
                this.batchAction = 'start_over_entirely'
                this.$nextTick(function() {
                    this.$refs.batchActionForm.submit()
                })
            },

            // startOverCustomer(confirmed) {
            //     if (!confirmed) {
            //         let msg = "Are you sure you want to start over for the customer data?"
            //         if (!confirm(msg)) {
            //             return
            //         }
            //     }
            //     this.customerIsKnown = true
            //     this.customerUUID = null
            //     // this.customerEntry = null
            //     this.phoneNumberEntry = null
            //     this.customerName = null
            //     this.phoneNumber = null
            // },

            // startOverItem(confirmed) {
            //     if (!confirmed) {
            //         let msg = "Are you sure you want to start over for the item data?"
            //         if (!confirm(msg)) {
            //             return
            //         }
            //     }
            //     // TODO: reset things
            // },

            cancelOrder() {
                let msg = "Are you sure you want to cancel?\n\n"
                    + "This will totally delete the current order."
                if (!confirm(msg)) {
                    return
                }
                this.batchAction = 'delete_batch'
                this.$nextTick(function() {
                    this.$refs.batchActionForm.submit()
                })
            },

            submitBatchData(params, callback) {
                let url = ${json.dumps(request.current_route_url())|n}
                
                let headers = {
                    ## TODO: should find a better way to handle CSRF token
                    'X-CSRF-TOKEN': this.csrftoken,
                }

                ## TODO: should find a better way to handle CSRF token
                this.$http.post(url, params, {headers: headers}).then((response) => {
                    if (callback) {
                        callback(response)
                    }
                })
            },

            setCustomerData() {
                let params = {
                    action: 'set_customer_data',
                    customer_uuid: this.customerUUID,
                    phone_number: this.phoneNumberEntry,
                }
                let that = this
                this.submitBatchData(params, function(response) {
                    that.phoneNumberSaved = true
                })
            },

            submitOrder() {
                alert("okay then!")
            },

            customerChanged(uuid) {
                if (!uuid) {
                    this.phoneNumberEntry = null
                    this.setCustomerData()
                } else {
                    let params = {
                        action: 'get_customer_info',
                        uuid: this.customerUUID,
                    }
                    let that = this
                    this.submitBatchData(params, function(response) {
                        that.phoneNumberEntry = response.data.phone_number
                        that.setCustomerData()
                    })
                }
            },

            phoneNumberChanged(value) {
                this.phoneNumberSaved = false
            },

            phoneNumberKeyDown(event) {
                if (event.which == 13) { // Enter
                    this.setCustomerData()
                }
            },
        },
    }

    Vue.component('customer-order-creator', CustomerOrderCreator)

  </script>
</%def>


${parent.body()}

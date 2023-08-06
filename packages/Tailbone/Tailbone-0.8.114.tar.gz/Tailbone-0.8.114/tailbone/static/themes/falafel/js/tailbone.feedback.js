
let FeedbackForm = {
    props: ['action'],
    template: '#feedback-template',
    methods: {

        showFeedback() {
            this.message = ''
            this.showDialog = true
            this.$nextTick(function() {
                this.$refs.textarea.focus()
            })
        },

        sendFeedback() {

            let params = {
                referrer: this.referrer,
                user: this.userUUID,
                user_name: this.userName,
                message: this.message.trim(),
            }

            let headers = {
                // TODO: should find a better way to handle CSRF token
                'X-CSRF-TOKEN': this.csrftoken,
            }

            this.$http.post(this.action, params, {headers: headers}).then(({ data }) => {
                if (data.ok) {
                    alert("Message successfully sent.\n\nThank you for your feedback.")
                    this.showDialog = false
                } else {
                    alert("Sorry!  Your message could not be sent.\n\n"
                          + "Please try to contact the site admin some other way.")
                }
            })
        },
    }
}

let FeedbackFormData = {
    referrer: null,
    userUUID: null,
    userName: null,
    message: '',
    showDialog: false,
}

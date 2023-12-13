var app = new Vue({
    el: '#app',
    delimiters: ['[%', '%]'],
    data: {
        invoice_amount: null,
        next_button_disabled: true,
        inn: default_inn,
        kpp: default_kpp,
        address: default_address,
        search_title: '',
        jobs_list: [],
        status: '',
        call_modal: '',
        selected_job_id: null,
        selected_payment_method: null,
        is_pay_button_active: false,
        price_ruble: const_price_ruble,
        price_bonus: const_payment_bonus_point_price,
        balance_ruble: const_balance_ruble,
        balance_bonus: const_balance_bonus,
        seen_empty_wallet: false,
        seen_empty_bonus: false,
    },
    methods: {
        do_create_new_tinkoff_card_payment: async function () {
            const res = await fetch(
                url_new_tinkoff_card_payment,
                {
                    method: 'POST',
                    body: JSON.stringify(
                        {
                            amount: this.invoice_amount
                        }
                    )
                }
            )
            const js = await res.json()
            window.open(js.invoice_url)
        },
        date_to_local: function (dt) {
            const date = new Date(dt)
            return date.toLocaleDateString()
        },
        load_jobs: async function () {
            const res = await fetch(
                url_jobs_list_api,
                {
                    method: 'post',
                    body: JSON.stringify(
                        {
                            title: this.search_title,
                            status: this.status,
                        }
                    )
                }
            )

            this.jobs_list = (await res.json()).jobs_list
            console.log(this.jobs_list)
        },
        pay_new_job: function () {
            let l = this.jobs_list.length;
            var jobid;
            for (let i = 0; i < l; ++i) {
                if (this.jobs_list[i].status === 'need_to_paid') {
                    jobid = this.jobs_list[i].id
                }
            }
            this.selected_job_id = jobid
            this.show_pay_modal(jobid)
        },

        reload: function () {
            location.reload()

        },

        show_paid_action: function () {
            const paidModal= new bootstrap.Modal(document.getElementById('paid_modal'))
            paidModal.show()
        },

        hide_paid_action: function () {
            const paidModal= new bootstrap.Modal(document.getElementById('paid_modal'))
            paidModal.hide()
        },

        show_pay_modal: function (job_id) {
            this.selected_job_id = job_id
            const myModal = new bootstrap.Modal(document.getElementById('pay_for_job_modal'))
            myModal.show()
        },

        hide_pay_model: function () {
            const myModal = new bootstrap.Modal(document.getElementById('pay_for_job_modal'))
            myModal.hide()
        },
        change_payment_method: function (method_name) {
            this.selected_payment_method = method_name;
            this.is_pay_button_active = true
        },

        do_pay_for_job: async function () {
            console.log(this.selected_payment_method)
            const res = await fetch(
                url_pay_for_job_api,
                {
                    method: 'post',
                    body: JSON.stringify(
                        {
                            job_id: this.selected_job_id,
                            balance_type: this.selected_payment_method,
                        }
                    )
                }
            )

            if (this.selected_payment_method === 'ruble' && this.balance_ruble < this.price_ruble) {
                this.seen_empty_wallet = true
                this.seen_empty_bonus = false
            }
            else if (this.selected_payment_method === 'bonus_point' && this.balance_bonus < this.price_bonus) {
                this.seen_empty_bonus = true
                this.seen_empty_wallet = false


            }
            else {
                this.show_paid_action()
            }

        },


    },

    watch: {
        invoice_amount: function () {
            if (this.invoice_amount)
                if (this.invoice_amount > 0) {
                    this.next_button_disabled = false
                    return
                }
            this.next_button_disabled = true
        },
        jobs_list: function () {
            const myModal1 = new bootstrap.Modal(document.getElementById('need_to_pay_warning_modal'))
            var show_warning_modal = false;

            const myModal2 = new bootstrap.Modal(document.getElementById('pxp-edit-admin-modal'))
            var show_admin_modal = false;

            this.jobs_list.forEach(
                function (job) {
                    if (job.status === 'need_to_paid') {
                        show_warning_modal = true;
                    }
                    if (job.call_modal === 'true'){
                        show_admin_modal = true
                    }
                }
            )
            if (show_warning_modal)
                myModal1.show()
        }
    },
    created: async function () {
        await this.load_jobs()
    }
})


const host = 'http://127.0.0.1:7788'
var App = {
    data() {
        return {
            update_dialog: false,
            id_to_update: null,
            method: null,
            url: null,
            exp: null,
            content_type: null,
            extract_type: null,
            rule_name: null,
            extract_method: null,
            crawl_name: null,
            current_callback: null,
            output: null,
            crawl_id:null,
            method_list: ['post', 'get'],
            tableData: []

        };
    },
    mounted() {
        this.search()
    },
    methods: {
        search() {
            const loading = this.$loading({
                lock: true,
                text: 'searching...',
                spinner: 'el-icon-loading',
                background: 'rgba(0, 0, 0, 0.7)'
            });

            axios.get(host + '/api/search', {}).then((response) => {
                data = response.data
                this.tableData = data
                console.log(this.tableData)
                loading.close()
            }).catch((err) => {
                loading.close()
                this.$message.error('search fail!')
            })
        },
        show_update_dialog(index, row) {
            console.log(row)
            this.method = row['rules']['method']
            this.url = row['rules']['url']
            this.rule_name = row['name']
            this.exp = row['parse']['crawl']['exp']
            this.extract_method = row['parse']['crawl']['extract_method']
            this.crawl_name = row['parse']['crawl']['name']
            this.current_callback = row['parse']['crawl']['current_callback']
            this.output = row['parse']['crawl']['output']
            this.extract_type = row['parse']['crawl']['extract']
            this.content_type = row['parse']['crawl']['type']
            this.id_to_update = row['_id']
            this.crawl_id = row['crawl_id']
            this.update_dialog = true

        },
        do_update_seed() {
            const _data = {
                method: this.method,
                url: this.url,
                rule_name: this.rule_name,
                exp: this.exp,
                extract_method: this.extract_method,
                crawl_name:this.crawl_name,
                current_callback:this.current_callback,
                output:this.output,
                extract_type:this.extract_type,
                crawl_id:this.crawl_id,
                content_type:this.content_type,
                id_to_update:this.id_to_update
            }
            console.log(_data)
            axios.post(host + '/api/update1', _data).then((response) => {
                success = response.data['success']
                if (success) {
                    this.search()
                    this.update_dialog = false.
                    return
                } else {
                    this.$notify({
                        title: 'update Fail',
                    })
                    return
                }
            }).catch((err) => {
                console.log(err)
            })
        },
        delete_info(index, row) {
            console.log(index, row)
            if (confirm('Do you really want to delete this rule?')) {
                axios.post(host + '/api/delete', {id: row['_id']}).then((response) => {
                    data = response.data
                    success = data['success']
                    if (success) {
                        this.search()
                        return
                    } else {
                        this.$notify({
                            title: 'delete Fail',
                        })
                        return
                    }
                }).catch((err) => {
                    console.log(err)
                })
            }

        }
    }
};
const app = Vue.createApp(App);
app.use(ElementPlus);
app.mount("#app");
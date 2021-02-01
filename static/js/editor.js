$(function () {
   let editor = $(".editor textarea");
   // make editor textarea's height auto-grow
   editor
      .on("input", (e) => {
         e.target.style.height = ""; /* Reset the height*/
         e.target.style.height = e.target.scrollHeight + "px";
      })
      .trigger("input");
   $(window).on("resize", (e) => {
      editor.trigger("input");
   });
});
// tinymce.get('emailContent').setContent('...');
// var content = tinymce.get('emailContent').getContent();
function getBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });
}

var app = new Vue({
    el: '#app',
    data: {
      other: '',
        loading: false,
        previewVisible:false,
        previewImage:"",
        // preview_banner_url:"",
        save_draft_model_visible: false,
        save_draft_loading: false,
        save_draft_button_loading: false,
        upload_loading:false,
        restore_draft_drawer_visible:false,
        preview_draft_drawer_visible: false,
        note: "",
        preview_draft_loading:false,
        preview_manual_draft_list:[],
        preview_auto_draft_list:[],
        preview_hot_draft_list: [],

        draft_status_key:"2",
        preview_draft_id:"",
        radioStyle: {
            display: 'block',
            height: '30px',
            lineHeight: '30px',
          },
      form: {
        banner:[],
        tags: undefined,
        groups: undefined,
        access_status: 0,
        password: '',
        show_comment: true,
        allow_comment: true,
      },
      rules:{
          password: { required: true, message: '文章密码不能为空哦~', trigger: 'blur' },
      }
    },
    delimiters: ['{[', ']}'],
    mounted() {
        if(is_edit){
            this.get_article_info()
        }else{
            this.init_editor()
        }
    },
    methods:{
        init_editor(){
            const editor = tinymce.init({
                selector: '#editor',
                //会自动引入link插件
                // https://fe.120yibao.com/common/tinymce/5.0.13/plugins/link/plugin.min.js
                //会自动引入silver主题
                // https://fe.120yibao.com/common/tinymce/5.0.13/themes/silver/theme.min.js
                theme: 'silver',
                //会自动引入oxide皮肤
                // https://fe.120yibao.com/common/tinymce/5.0.13/skins/ui/oxide/skin.min.css
                skin: "oxide",
                language: 'zh_CN',
                paste_data_images: true,
                codesample_global_prismjs: true,
                plugins: [
                  'advlist autolink link image lists charmap print preview hr anchor pagebreak spellchecker',
                  'searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking',
                  'save table directionality emoticons template paste codesample'
                ],
                codesample_languages: [
                    {text: 'Python', value: 'python'},
                    {text: 'HTML/XML', value: 'markup'},
                    {text: 'JavaScript', value: 'javascript'},
                    {text: 'CSS', value: 'css'},
                    {text: 'Bash/Shell', value: 'shell'},
                    {text: 'PHP', value: 'php'},
                    {text: 'Perl', value: 'perl'},
                    {text: 'Go', value: 'go'},
                    {text: 'PowerShell', value: 'powershell'},
                    {text: 'nginx', value: 'nginx'},
                    {text: 'Java', value: 'java'},
                    {text: 'Json', value: 'json'},
                    {text: 'Makefile', value: 'makefile'},
                    {text: 'Markdown', value: 'markdown'},

                    {text: 'Ruby', value: 'ruby'},
                    {text: 'Java', value: 'java'},
                    {text: 'C', value: 'c'},
                    {text: 'C#', value: 'csharp'},
                    {text: 'C++', value: 'cpp'}
                ],
                toolbar: 'insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link codesample | print preview media fullpage | forecolor backcolor emoticons'
            });
        },
        get_article_info(){
            let that = this;
            $.ajax({
                type: 'GET',
                url: '/api/article/editor/'+article_id+'/',
                headers:{
                    'token': Cookies.get('token')
                },
                success: function (data) {
                    if (data.code===0) {
                        $('#title').val(data.data.title);
                        $('#editor').val(data.data.content);
                        that.init_editor();
                        that.form.access_status = data.data.access_status;
                        that.form.allow_comment = data.data.allow_comment;
                        that.form.show_comment = data.data.show_comment;
                        that.form.password = data.data.password;
                        that.form.tags = data.data.tag;
                        that.form.groups = data.data.group;
                        that.$set(that.form, 'banner', [{
                                uid: '-1',
                                name: 'default.jpg',
                                url: data.data.banner,
                                response:{
                                    url: data.data.banner
                                },
                                status: 'done',
                            }]);
                        console.log(JSON.stringify(that.form.banner))
                        that.previewImage = data.data.banner

                    } else {
                        antd.message.error(data.msg)
                    }

                },
                error: function (error) {
                    try {
                        let response = JSON.parse(error.responseText);
                        if (response.msg) {
                            antd.message.error(response.msg);
                        } else {
                            antd.message.error(error.statusText);
                        }
                    } catch (e) {
                        antd.message.error(error.statusText);
                    }
                }
            });
        },
        delete_article(){
            this.$confirm({
                title: '警告',
                okText: '确认删除',
                cancelText: '取消',
                content: '删除后将无法恢复，确认删除此文章 ？',
                onOk() {
                    $.ajax({
                        type: 'DELETE',
                        url: '/api/article/editor/'+article_id+'/',
                        headers:{
                            'token': Cookies.get('token')
                        },
                        success: function (data) {
                            antd.message[data.code===0 ? 'success': 'error'](data.msg)
                            if (data.code===0){
                                setTimeout(function () {
                                    window.location.href = '/'
                                }, 1000)
                            }
                        },
                        error: function (error) {
                            try {
                                let response = JSON.parse(error.responseText);
                                if (response.msg) {
                                    antd.message.error(response.msg);
                                } else {
                                    antd.message.error(error.statusText);
                                }
                            } catch (e) {
                                antd.message.error(error.statusText);
                            }
                        }
                    });
                },
                onCancel() {
                },
            });
        },
        save_draft(){
            this.save_draft_model_visible = true;
        },
        restore_draft(){
            this.getDraft();
            this.restore_draft_drawer_visible = true;
        },
        handleSaveModelOk(e) {
            this.save_draft_loading = true;
            let content = tinymce.get('editor').getContent();
            let that = this;
            $.ajax({
                type: 'POST',
                url: '/api/article/draft/',
                headers:{
                    'token': Cookies.get('token')
                },
                data:{
                    article_id: article_id,
                    content: content,
                    type: 1,
                    note: this.note,
                    title: $('#title').val()
                },
                success: function (data) {
                    if (data.code===0) {
                        antd.message.success(data.msg)
                        setTimeout(() => {
                            that.save_draft_model_visible = false;
                        }, 400);
                    } else {
                        antd.message.error(data.msg)
                    }
                },
                error: function (error) {
                    try {
                        let response = JSON.parse(error.responseText);
                        if (response.msg) {
                            antd.message.error(response.msg);
                        } else {
                            antd.message.error(error.statusText);
                        }
                    } catch (e) {
                        antd.message.error(error.statusText);
                    }
                }
            });
            this.save_draft_loading = false;

        },
        handleSaveModelCancel(){
            this.save_draft_model_visible = false
        },
        RestoreDraftDrawerClose(){
            this.restore_draft_drawer_visible = false
        },
        RestoreDraftDrawerSubmit(){
            let that = this;
            if(!this.preview_draft_id&&this.draft_status_key!=="2"){
                if(this.draft_status_key==="0"){
                    if(this.preview_auto_draft_list.length===0){
                        antd.message.error("恢复失败，当前文章还没有自动保存任何草稿哦");
                    }else{
                        antd.message.error("请先选择要恢复的草稿");
                    }
                }else if(this.draft_status_key==="1"){
                    if(this.preview_manual_draft_list.length===0){
                        antd.message.error("恢复失败，当前文章还没有手动保存过任何草稿哦");
                    }else{
                        antd.message.error("请先选择要恢复的草稿");
                    }
                }
                return false
            }
            this.save_draft_button_loading = true;
            $.ajax({
                type: 'GET',
                url: '/api/article/draft/detail/',
                headers:{
                    'token': Cookies.get('token')
                },
                data:{
                    article_id: article_id,
                    type: this.draft_status_key,
                    draft_id: this.preview_draft_id
                },
                success: function (data) {
                    if (data.code===0) {
                        that.$confirm({
                            title: '警告',
                            okText: '确认恢复',
                            cancelText: '取消',
                            content: '恢复草稿将会覆盖当前编辑器里的内容，请注意是否有需要保存的信息，确认进行此操作吗？',
                            onOk() {
                                antd.message.success("恢复成功");
                                $('#title').val(data.data.title);
                                tinymce.get('editor').setContent(data.data.content);
                                that.preview_draft_loading = false;
                                that.restore_draft_drawer_visible = false;
                                that.save_draft_button_loading = false;

                            },
                            onCancel() {
                                that.preview_draft_loading = false;
                                that.save_draft_button_loading = false;

                            },
                        });
                    } else {
                        antd.message.error(data.msg);
                        that.save_draft_button_loading = false;

                    }
                },
                error: function (error) {
                    try {
                        let response = JSON.parse(error.responseText);
                        if (response.msg) {
                            antd.message.error(response.msg);
                        } else {
                            antd.message.error(error.statusText);
                        }
                    } catch (e) {
                        antd.message.error(error.statusText);
                    }
                    this.save_draft_button_loading = false;
                }
            });


        },
        PreviewDraftDrawerOpen(){
            $('#preview-draft').html('');
            this.preview_draft_drawer_visible = true;
            this.preview_draft_loading = true;
            let that = this;
            $.ajax({
                type: 'GET',
                url: '/api/article/draft/detail/',
                headers:{
                    'token': Cookies.get('token')
                },
                data:{
                    article_id: article_id,
                    type: this.draft_status_key,
                    draft_id: this.preview_draft_id
                },
                success: function (data) {
                    if (data.code===0) {
                        $('#preview-draft-title').html(data.data.title);
                        $('#preview-draft').html(data.data.content);
                        Prism.highlightAll();
                    } else {
                        antd.message.error(data.msg)
                    }
                    that.preview_draft_loading = false;

                },
                error: function (error) {
                    try {
                        let response = JSON.parse(error.responseText);
                        if (response.msg) {
                            antd.message.error(response.msg);
                        } else {
                            antd.message.error(error.statusText);
                        }
                    } catch (e) {
                        antd.message.error(error.statusText);
                    }
                    that.preview_draft_loading = false;
                }
            });
        },
        PreviewDraftDrawerClose(){
            this.preview_draft_drawer_visible = false
        },
        getDraft(){
            let that = this;
            $.ajax({
                type: 'GET',
                url: '/api/article/draft/',
                headers:{
                    'token': Cookies.get('token')
                },
                data:{
                    article_id: article_id,
                    type: this.draft_status_key,
                },
                success: function (data) {
                    if (data.code===0) {
                        if(that.draft_status_key==="2"){
                            that.preview_hot_draft_list = data.list
                        }else if(that.draft_status_key==="1"){
                            that.preview_manual_draft_list = data.list
                        }else if(that.draft_status_key==="0"){
                            that.preview_auto_draft_list = data.list
                        }
                    } else {
                        antd.message.error(data.msg)
                    }

                },
                error: function (error) {
                    try {
                        let response = JSON.parse(error.responseText);
                        if (response.msg) {
                            antd.message.error(response.msg);
                        } else {
                            antd.message.error(error.statusText);
                        }
                    } catch (e) {
                        antd.message.error(error.statusText);
                    }
                }
            });
        },
        handleUploadPreviewBannerCancel(){
            this.previewVisible = false
        },
        DraftTabChange(){
            this.preview_draft_id="";
            this.getDraft()
        },
        PreviewDraftChange(e){
            this.PreviewDraftDrawerOpen(e.target.value)
        },
        handleUploadPreviewBannerChange({ fileList }){
            fileList.forEach(function (item) {
                if(item.status===undefined){
                    item.status = 'error'
                }
            });
            this.form.banner = fileList;
        },
        async handleUploadPreviewBannerPreview(file){
            if (!file.url && !file.preview) {
                file.preview = await getBase64(file.originFileObj);
            }
            this.previewImage = file.url || file.preview;
            this.previewVisible = true;
        },
        beforeUploadPreviewBanner(file){
            const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
            if (!isJpgOrPng) {
                this.$message.error('仅支持jpg和png格式的图片');
            }
            const isLt10M = file.size / 1024 / 1024 < 10;
            if (!isLt10M) {
                this.$message.error('为了加载速度，请上传小于10MB大小的图片');
            }
            let result = [];
            this.form.banner.forEach(function (item) {
                if(item.status){
                    result.push(item)
                }
            });
            this.form.banner = result;
            return isJpgOrPng && isLt10M;
        },
        submit(){
            let that = this;
            let banner = '';
            if(this.form.access_status===2&&!this.form.password){
                antd.message.error("密码不得为空哦~");
                return false;
            }
            if(that.form.banner.length>0){
                banner = that.form.banner[0];
                if(banner.status==='error'){
                    that.$confirm({
                        title: '警告',
                        okText: '确认提交',
                        cancelText: '取消',
                        content: '当前上传的封面是无效的资源，继续提交将使用随机图片作为文章封面，是否继续？',
                        onOk() {
                            if(is_edit){
                                that.do_update('')
                            }else{
                                that.do_create('')
                            }
                        },
                        onCancel() {
                            antd.message.info('已取消提交');
                            return false
                        },
                    });
                }else{
                    if(is_edit){
                        that.do_update(banner.response.url)
                    }else{
                        that.do_create(banner.response.url)
                    }
                }
            }else{
                if(is_edit){
                    that.do_update('')
                }else{
                    that.do_create('')
                }
            }
        },
        do_create(banner){
            let that = this;
            let content = tinymce.get('editor').getContent();

            $.ajax({
                type: 'POST',
                url: '/api/article/',
                headers:{
                    'token': Cookies.get('token')
                },
                data:{
                    title: $('#title').val(),
                    content: content,
                    tags: JSON.stringify(that.form.tags),
                    groups: JSON.stringify(that.form.groups),
                    access_status: that.form.access_status,
                    password: that.form.password,
                    banner: banner,
                    show_comment: that.form.show_comment,
                    allow_comment: that.form.allow_comment,
                },
                success: function (data) {
                    if (data.code===0) {
                        antd.message.success(data.msg);
                        setTimeout(function () {
                            window.location.href=data.redirect
                        }, 700)
                    } else {
                        antd.message.error(data.msg);
                    }
                },
                error: function (error) {
                    try {
                        let response = JSON.parse(error.responseText);
                        if (response.msg) {
                            antd.message.error(response.msg);
                        } else {
                            antd.message.error(error.statusText);
                        }
                    } catch (e) {
                        antd.message.error(error.statusText);
                    }
                }
            })
        },
        do_update(banner){
            let that = this;
            let content = tinymce.get('editor').getContent();

            $.ajax({
                type: 'PUT',
                url: '/api/article/editor/'+article_id+'/',
                headers:{
                    'token': Cookies.get('token')
                },
                data:{
                    title: $('#title').val(),
                    content: content,
                    tags: JSON.stringify(that.form.tags),
                    groups: JSON.stringify(that.form.groups),
                    access_status: that.form.access_status,
                    password: that.form.password,
                    banner: banner,
                    show_comment: that.form.show_comment,
                    allow_comment: that.form.allow_comment,
                },
                success: function (data) {
                    if (data.code===0) {
                        antd.message.success(data.msg);
                    } else {
                        antd.message.error(data.msg);
                    }
                },
                error: function (error) {
                    try {
                        let response = JSON.parse(error.responseText);
                        if (response.msg) {
                            antd.message.error(response.msg);
                        } else {
                            antd.message.error(error.statusText);
                        }
                    } catch (e) {
                        antd.message.error(error.statusText);
                    }
                }
            })
        }

    },
    created(){

    }
});


$('input').on('input', function(){
  var pwf = $('.pw-fancy--asterisks'),
      pwLength = $(this).val().length;
  $('.pw-fancy').removeClass('warning');
  // check pw length
  if( pwLength > pwf.children().length){
    // add an asterisk if pw length has increased
    pwf.append('<i class="fa fa-asterisk"></i>');
  } else if (pwLength < pwf.children().length){
    // remove the last asterisk until length is same or lower
    while(pwLength < pwf.children().length){
      // todo, remove animation?
      pwf.children().last().remove();
    }
  }
  // some responsive styling, there's probably a better way to do this :P
  if(pwLength > 8){
    pwf.addClass('pw-long');
  } else {
    pwf.removeClass('pw-long');
  }
  if(pwLength > 16){
    pwf.addClass('pw-longer');
  } else {
    pwf.removeClass('pw-longer');
  }
});
$('#article_password').focus()

$('.check-password').click(function(){
    let article_id = $('#article_id').val();
    let password = $('#article_password').val();
    if(password&&article_id) {
        $.ajax({
            type: 'POST',
            url: '/api/article/' + article_id + '/verify/',
            headers: {
                'token': Cookies.get('token')
            },
            data: {
                article_id: article_id,
                password: password
            },
            success: function (data) {
                if (data.status) {
                    Cookies.set(article_id + '_password', password)
                    location.reload()
                } else {
                    $('.pw-fancy').toggleClass('warning');
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
    }else{
        antd.message.error('密码不能为空哦~ 😯')
    }
});

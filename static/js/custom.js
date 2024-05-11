$( document ).ready(function() {
    

});

function comment(id){
    $(".comment_message_"+id).toggleClass('d-none')
}

function submit_commeent(id){
    var id_post = id
    var com_msg = $('#comment_message_'+id).val()
    if(com_msg === ''){
        return false;
    }
    $.ajax({
        url : '/save-comment/',
        type : 'post',
        data : {'comment_msg':com_msg,'blog_id':id},
        success : function(res){
            var data = res
            var com_msg = $('#comment_message_'+id).val('')
            
            $('.count_comment_of_'+id_post).addClass('comm_wrap')
            $('.count_comment_of_'+id_post).text(data.count_val)
            $(".list_blog_c_"+id_post).prepend(data.html_com);
        }
    })
}

function submit_like(id){
    var id_post = id
    var tag_1 = $('.check_like_cls_'+id_post).hasClass('like')
    if(tag_1){
        $('.check_like_cls_'+id_post).removeClass('like')
        var type_like = "dislike"
    }
    else{
        $('.check_like_cls_'+id_post).addClass('like')
        var type_like = "like"
    }
    $.ajax({
        url : '/save-like/',
        type : 'post',
        data : {'type_like':type_like,'blog_id':id_post},
        success : function(res){
            $('.like_total_'+id_post).text(res.count_val)
            
        }
    })
}


$(document).ready(function(){
    $(".share_button_action").click(function(){
        var blogId = $(this).data('blog_id');
        $(".blog_id_data").val(blogId)
    });
  });

  


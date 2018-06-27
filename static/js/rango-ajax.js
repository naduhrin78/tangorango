$('#likes').click(function () {
    var cat_id;

    cat_id = $(this).attr('data-catid');

    $.get('/rango/like_category/', {category_id:cat_id}, function (data) {
        $('#likes_count').html(data+' People liked this category.');
        $('#likes').hide();
        $('#dislikes').show();
    })


});

$('#dislikes').click(function () {
    var cat_id;

    cat_id = $(this).attr('data-catid');

    $.get('/rango/dislike_category/', {category_id:cat_id}, function (data) {
        $('#likes_count').html(data + ' People liked this category.');
        $('#likes').show();
        $('#dislikes').hide();
    })


});

$('#suggestion').keyup(function(){
    var query;
    query = $(this).val();
    $.get('/rango/suggest_category/', {suggestion: query}, function(data){
        $('#cats').html(data);
    });
});
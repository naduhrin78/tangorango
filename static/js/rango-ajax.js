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

$('.add_search').click(
    function () {
        var me = $(this);
        var url = $(this).attr("data-url");
        var title = $(this).attr("data-title");
        var csrf = $(this).attr("csrf");
        var category = prompt("Please enter category");

        if(category)
        {
            $.get('/rango/search_cat/', {category: category}, function (data) {
                var cat = data;

                var agree;

                if(cat == "new")
                {
                    agree = confirm("Add new category?");

                    if(agree)
                    {
                        $.post('/rango/add_category/', {csrfmiddlewaretoken: csrf, views: 0, likes: 0, slug: 0, name: category, submit: "Create category"},function (data) {
                            me.hide();
                        });
                    }
                }

                agree = confirm("Add to "+category+"?");

                $.get('/rango/search_cat/', {category: category}, function (data) {

                    cat = data;

                    if (agree) {
                        $.post('/rango/category/' + cat + '/add_page/', {
                            csrfmiddlewaretoken: csrf,
                            title: title,
                            url: url,
                            views: 0,
                            slug: 0,
                            category: category,
                            submit: "Create Page"
                        }, function (data) {
                            me.hide();
                        });
                    }
                });

            });

        }

    }

);
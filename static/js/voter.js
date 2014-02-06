$(document).ready(function()
{
    $('ul.messages').fadeOut(2000);
    update()
    setInterval(update, 5000);

    function update()
    {
        $.getJSON("update", updateNowPlaying);
    }

    function updateNowPlaying(data)
    {
        if (!data.current)
            return false;

        var nowPlaying = $('#nowplaying');
        nowPlaying.empty()
        $('<span>').html('Now playing:' + data.current.title + ' - ' + data.current.artist)
                .addClass('title')
        .appendTo(nowPlaying);


        return updateQueue(data)
    }

    function updateQueue(data) {
        if (!data.queue)
            return false;

        var queue = $('#queue');

        queue.data('ts', new Date().getTime()).empty();
        $.each(data.queue, function (index, song) {

            var listItem = $('<li>').addClass('list-group-item');

            $('<span>').html(song.title + ' - ' + song.artist)
                .addClass('title')
                .appendTo(listItem);

            $('<button>')
                 .addClass('btn btn-success btn-style')
                 .addClass('upvote-button')
                 .addClass('pull-right')
                 .html('<span class="glyphicon glyphicon-plus"></span>')
                 .attr({ type: 'button', id: song.id , value:'upvote'})
                 .appendTo(listItem)

             $('<button>')
                 .addClass('btn btn-danger btn-style')
                 .addClass('downvote-button')
                 .addClass('pull-right')
                 .html('<span class="glyphicon glyphicon-minus"></span>')
                 .attr({ type: 'button', id: song.id , value:'downvote'})
                 .appendTo(listItem)


            $('<span>').attr('title', 'Number of votes')
                .addClass('badge')
                .html((song.queue < 0) ? 'Random' : song.queue + ' ' + ((song.queue > 1) ? 'votes' : 'vote'))
                .appendTo(listItem);


            queue.append(listItem)


        });

        return true;

    }

    $(document).on('click', ".upvote-button", function (e) {
        e.preventDefault();

        jQuery.ajax(
        {
            'type': 'POST',
            'url': 'upvote/',
            'data': { 'songId': $(this).attr('id')},
            'dataType': 'json',
            'success': updateQueue
        });
     });

    $(document).on('click', ".downvote-button", function (e) {
        e.preventDefault();

        jQuery.ajax(
        {
            'type': 'POST',
            'url': 'downvote/',
            'data': { 'songId': $(this).attr('id')},
            'dataType': 'json',
            'success': updateQueue
        });
     });

    $(document).on('click', ".downvote-button", function (e) {
        e.preventDefault();

        jQuery.ajax(
        {
            'type': 'POST',
            'url': 'downvote/',
            'data': { 'songId': $(this).attr('id')},
            'dataType': 'json',
            'success': updateQueue
        });
     });

     $('#SearchForm').submit(function() {
        jQuery.ajax(
        {
            type: $(this).attr('method'),
            'url': $(this).attr('action'),
            'data': $(this).serialize(),
            'success': showResults
        });

     });

    function showResults(data)
    {

        var modal = $('<div>').attr('id', 'searchResultModal')
                .addClass('modal')
                .addClass('fade');

        modal.on('hidden.bs.modal', function () {
             $(this).remove();
        })
        .modal()
        data.trigger('loaded.bs.modal');


    }
});
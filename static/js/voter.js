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
        $('<span>').html(data.current.title + ' - ' + data.current.artist)
                .addClass('title')
        .appendTo(nowPlaying);


        return updateQueue
    }

    function updateQueue(data) {
        if (!data.queue)
            return false;

        var queue = $('#quaue');

        queue.data('ts', new Date().getTime()).empty();
        $.each(data.queue, function (index, song) {

            var listItem = $('<li>').addClass('list-group-item');

            $('<span>').html(song.title + ' - ' + song.artist)
                .addClass('title')
                .appendTo(listItem);

            $('<button>')
                 .addClass('btn btn-success btn-style')
                 .addClass('upvote-button')
                 .attr({ type: 'button', id: song.id , value:'upvote'})
                 .appendTo(listItem)

             $('<button>')
                 .addClass('btn btn-success btn-style')
                 .addClass('downvote-button')
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
}
);
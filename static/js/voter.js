$(document).ready(function()
{
    $('#messages').fadeOut(10000);
    update()
    setInterval(update, 5000);

    function update()
    {
        $.getJSON("/voter/update", updateNowPlaying);
    }

    function updateNowPlaying(data)
    {
        if (!data.current)
            return false;

        var nowPlaying = $('#nowplaying');
        nowPlaying.empty()
        $('<span>').html('Now playing: ' + data.current.title + ' - ' + data.current.artist)
                .addClass('title')
        .appendTo(nowPlaying);


        return updateQueue(data)
    }

    function updateQueue(data) {
        if (!data.queue)
            return false;



        var queue = $('#queue');

        var voteStatus = $('#vote-status-container');
        voteStatus.empty()
        $('<button>')
            .prop('disabled',true)
            .addClass('btn btn-lg pull-right')
            .addClass((data.ableToVote == true) ? 'btn-success' : 'btn-danger')
            .html((data.ableToVote == true)? '1 Vote' : '0 Votes')
            .appendTo(voteStatus)


        queue.data('ts', new Date().getTime()).empty();
        $.each(data.queue, function (index, song) {

            var listItem = $('<li>').addClass('list-group-item');

            $('<button>')
            .addClass('btn btn-success btn-style btn-lg')
            .addClass('upvote-button')
            .addClass('pull-right')
            .prop('disabled',((data.ableToVote == false) ? true : false))
            .html('<span class="glyphicon glyphicon-plus"></span>')
            .attr({ type: 'button', id: song.id , value:'upvote'})
            .appendTo(listItem)
            /*
            $('<button>')
            .addClass('btn btn-danger btn-style btn-lg')
            .addClass('downvote-button')
            .addClass('pull-right')
            .prop('disabled',((data.ableToVote == false) ? true : false))
            .html('<span class="glyphicon glyphicon-minus"></span>')
            .attr({ type: 'button', id: song.id , value:'downvote'})
            .appendTo(listItem)
            */
            $('<span>').attr('title', 'Number of votes')
            .addClass('badge')
            .html((song.queue <= 0) ? '' : song.queue + ' ' + ((song.queue > 1) ? 'votes' : 'vote'))
            .appendTo(listItem);

            $('<span>').html('<div>' + song.title + '</div><div>' + song.artist + '</div>')
                .addClass('title')
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
            'url': '/voter/upvote/',
            'data': { 'songId': $(this).attr('id')},
            'dataType': 'json',
            'success': function(data){
                $('#searchResults').empty();
                $('#voter-container').css('display', 'block');
                updateQueue(data)
            }
        });
     });

    $(document).on('click', ".downvote-button", function (e) {
        e.preventDefault();

        jQuery.ajax(
        {
            'type': 'POST',
            'url': '/voter/downvote/',
            'data': { 'songId': $(this).attr('id')},
            'dataType': 'json',
            'success': function(data){
                $('#searchResults').empty();
                $('#voter-container').css('display', 'block');
                updateQueue(data)
            }
        });
     });

    $(document).on('submit', "#SearchForm", function (e) {
        e.preventDefault();

            var form = $(this);

            $.ajax({
                type: 'POST',
                data: form.serialize(),
                url: form.attr('action'),
                success: function(data) {
                    $('#searchResults').html(data);
                    $('#voter-container').css('display', 'none');

                }
            });
        });


    $(document).on('click', "#close-searchResults", function (e) {
        e.preventDefault();

        $('#searchResults').empty();
        $('#voter-container').css('display', 'block');

     });


});
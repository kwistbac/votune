$(function () {
    $('ul.messages').fadeOut(2000);

    function updateVoterQueue(data) {
        var queue = $('#queue');

        queue.data('ts', new Date().getTime()).empty();
        $.each(data.queue, function (index, song) {
            var item = $('<li>').addClass('list-group-item');
            $('<span>').html(song.title + ' - ' + song.artist)
                .addClass('title')
                .appendTo(item);
            $('<span>').attr('title', 'Number of votes')
                .addClass('badge')
                .html((song.queue < 0) ? 'Random' : song.queue + ' ' + ((song.queue > 1) ? 'votes' : 'vote'))
                .appendTo(item);
            queue.append(item)
        });

        return true;
    }

    function updateVoterSong(data) {
        if (!data.current)
            return false;

        var player = $('#player').get(0);
        player.src = data.current.url;
        player.play();

        $('#songTitle').html(data.current.title);
        $('#songArtist').html(data.current.artist);
        $('#songAlbum').html(data.current.album);
        if (data.current.image) {
            var img = $('<img>').attr('src', data.current.image);
            $('#songImage').empty().append(img);
        }
        else {
            var icon = $('<span>').addClass('glyphicon glyphicon-music');
            $('#playerImage').empty().append(icon);
        }

        return updateVoterQueue(data);
    }

    function updateVoter() {
                $.getJSON("voter/update", updateVoterSong);
    }

    updateVoter();
    setInterval(updateVoter, 1000);


});

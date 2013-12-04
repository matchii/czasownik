$('document').ready(function() {
    // nowy
    $('#new_task').live('click', function() {
        $.get('create/', {}, function(id) {
            if (id) {
                $('#task_list').append(
                    $('<li>').addClass('task_container').attr({'id': 'task_'+id+'_container', 'task-id': id})
                        .append(
                            $('<input>').attr({'type': 'text', 'maxlength': '255', 'size': 30, 'name': 'what'})
                        )
                        .append(
                            $('<button>')
                                .attr({'type': 'button'})
                                .addClass('start_time')
                                .text('Start')
                        )
                        .append(
                            $('<input>')
                                .attr({
                                    'id': 'task_'+id+'_from',
                                    'type': 'text',
                                    'maxlength': '5',
                                    'size': 3,
                                    'name': 'from_hour'
                                })
                                .addClass('time_input')
                        )
                        .append(
                            $('<button>')
                                .attr({'type': 'button'})
                                .addClass('stop_time')
                                .text('Stop')
                        )
                        .append(
                            $('<input>')
                                .attr({
                                    'id': 'task_'+id+'_to',
                                    'type': 'text',
                                    'maxlength': '5',
                                    'size': 3,
                                    'name': 'to_hour'
                                })
                                .addClass('time_input')
                        )
                        .append(
                            $('<button>')
                                .attr({'type': 'button'})
                                .addClass('save_button')
                                .text('Zapisz')
                        )
                        .append(
                            $('<button>')
                                .attr({'type': 'button'})
                                .addClass('delete_button')
                                .text('Usuń')
                        )
                        .append(
                            $('<span>')
                                .attr({'name': 'time'})
                        )
                )
            }
        })
    })
    // start
    $('.start_time').live('click', function() {
        var t = $(this)
        t.siblings('img').show()
        var id = t.parent().attr('task-id')
        var what = t.siblings('input[name="what"]').val()
        var from_hour = new Date().toTimeString().substr(0, 5)
        var to_hour = t.siblings('input[name="to_hour"]').val()
        $('#task_'+id+'_from').val(from_hour)
        $.get(
            'save/',
            { 'id': id, 'what': what, 'from_hour': from_hour, 'to_hour': to_hour },
            function(data) { t.siblings('img').hide() }
        )
    })
    // stop
    $('.stop_time').live('click', function() {
        var t = $(this)
        t.siblings('img').show()
        var id = $(this).parent().attr('task-id')
        var what = $(this).siblings('input[name="what"]').val()
        var from_hour = $(this).siblings('input[name="from_hour"]').val()
        var to_hour = new Date().toTimeString().substr(0, 5)
        $('#task_'+id+'_to').val(to_hour)
        $.getJSON(
            'save/',
            { 'id': id, 'what': what, 'from_hour': from_hour, 'to_hour': to_hour },
            function(data) {
                t.siblings('img').hide()
                t.siblings('span[name="delta"]').text(data.delta)
            }
        )
    })
    $('.save_button').live('click', function() {
        var t = $(this)
        t.siblings('img').show()
        var id = $(this).parent().attr('task-id')
        var what = $(this).siblings('input[name="what"]').val()
        var from_hour = $(this).siblings('input[name="from_hour"]').val()
        var to_hour = $(this).siblings('input[name="to_hour"]').val()
        $.getJSON(
            'save/',
            { 'id': id, 'what': what, 'from_hour': from_hour, 'to_hour': to_hour },
            function(data) {
                t.siblings('img').hide()
                t.siblings('span[name="delta"]').text(data.delta)
            }
        )
    })
    // usuwanie zadania
    $('.delete_button').live('click', function() {
        if (! confirm('Na pewno?')) {
            return
        }
        var id = $(this).parent().attr('task-id')
        $.getJSON('delete_task/', { 'id': id, 'action': 'delete_task' }, function(data) {
            if (data['success']) {
                var obj = $('#task_'+id+'_container')
                obj.fadeOut(300, function() { obj.remove() })
            }
        })
    })
    $('.time_input').live('keypress', function(event) {
        var charCode = (event.which) ? event.which : event.keyCode;
        // można wpisać :
        if (charCode == ':'.charCodeAt(0)) {
            return true
        }
        // poza tym dopuszczamy tylko cyfry
        if (charCode > 31 && (charCode < 48 || charCode > 57)) {
            return false
        } else {
            return true
        }
    })
});

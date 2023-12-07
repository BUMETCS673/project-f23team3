$(document).ready(function() {
    var socket = io()
    socket.on("connect", function () {
        socket.send("Client connected")
    });

    $('form#joinRoom').submit(function (event) {
        socket.emit('joinRoom', {
            secretkey: $('#secretkeyNum').val()
        })
        return false
    });

    socket.on('roomJoined', function (msg, cb) {
    $('#chatContent').append('<div class="chat-message"><b>' + msg.user + ' has joined the service center.</b></div>');
    });

    socket.on('roomLeftPersonal', function (msg, cb) {
        $('#chatContent').append('<div class="chat-message"><b>You have left the service center.</b></div>');
    });

    socket.on('roomLeft', function (msg, cb) {
        $('#chatContent').append('<div class="chat-message"><b>' + msg.user + ' has left the service center.</b></div>');
    });

    $('#leave_room').on('click', function () {
        socket.emit('leaveRoom', {
            secretkey: $('#secretkeyNum').val()
        });
        location.assign("/chat");
    });

    $('form#SubmitForm').submit(function(){
        socket.emit('sendMsg', {
            msg:$('#chatMsg').val(),
            secretkey:$('#secretkeyNum').val()
        });
        $('#chatMsg').val("");
        return false
    });

    socket.on('sendtoAll', function(msg, cb){
        $('#chatContent').append('<div class="chat-message"><b>' + msg.user + ':</b> ' + msg.msg + '</div>');
    });

    socket.on('Confserver', function (msg, cb) {
        $('#chatContent').append('<div class="chat-message"><b>' + msg.user + ':</b> <b><p style="color: green">Copy that, I am on my way.</p></b></div>');
    });

    $('#serverMsg').on('click', function () {
        socket.emit('serverConf', {
            secretkey: $('#secretkeyNum').val()
        });
    });

    socket.on('Conf_kitchen', function (msg, cb) {
        $('#chatContent').append('<div class="chat-message"><b>' + msg.user + ':</b> <b><p style="color: red">Please serve the dishes.</p></b></div>');
    });

    $('#kitchenMsg').on('click', function () {
        socket.emit('kitchenConf', {
            secretkey: $('#secretkeyNum').val()
        });
    });

})
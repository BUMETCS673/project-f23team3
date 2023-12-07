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
        $('#chatContent').append('<li>' + msg.user + ' has joined the service center' + '</li>')
    });

    socket.on('roomLeftPersonal', function (msg, cb) {
        $('#chatContent').append('<li>' + ' you have left the service center' + '</li>')
    });

    socket.on('roomLeft', function (msg, cb) {
        $('#chatContent').append('<li>' + msg.user + ' has left the service center' + '</li>')
    });

    $('#leave_room').on('click', function () {
        socket.emit('leaveRoom', {
            secretkey: $('#secretkeyNum').val()
        });
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
        $('#chatContent').append('<li>' + msg.user + ':' + msg.msg + '</li>')
    });

    socket.on('Confserver', function (msg, cb) {
        $('#chatContent').append('<li>' + msg.user + ':' + '<b><p style="color: green">copy that, I am on my way</p></b>' + '</li>')
    });

    $('#serverMsg').on('click', function () {
        socket.emit('serverConf', {
            secretkey: $('#secretkeyNum').val()
        });
    });

    socket.on('Conf_kitchen', function (msg, cb) {
        $('#chatContent').append('<li>' + msg.user + ':' + '<b> <p style="color: red">Please serve the dishes</p> </b>' + '</li>')

    });

    $('#kitchenMsg').on('click', function () {
        socket.emit('kitchenConf', {
            secretkey: $('#secretkeyNum').val()
        });
    });
})
console.log(`script.js`);

$(document).ready(function () {
  var socket = io.connect('http://localhost:5000');

  function log(msg) {
    $('#logs').prepend(`<pre>${msg}</pre>`);
  }

  socket.on('connect', function () {
    console.log('User has connected');
    socket.emit('my_event', {
      data: "I'm connected!",
      room: 'A'
    });
  });

  socket.on('my_response', function (msg, cb) {
    console.log(`Received message: ${msg}`);
    if (cb) {
      cb();
    }
  });

  socket.on('message', function (msg) {
    log(msg);
    console.log(msg);
    $('#currentPosition').val(msg);
  });

  /* Listen for info messages and push a toast notification */
  socket.on("info", function( msg, cb) {
    console.log("Received an info message: " + msg)
    const element = `
      <div id="${msg.guid}" class="toast" role="alert" data-delay="1000">
        <div class="toast-header">
          <strong class="mr-auto">${msg.type.toUpperCase()}</strong>
          <small class="text-muted">{{ msg.room }}</small>
          <button type="button" class="ml-2 mb-1 close" data-dismiss="toast">
            <span>&times;</span>
          </button>
        </div>
        <div class="toast-body">
          ${msg.memo}
        </div>
      </div>
    `;
    $("#toasts").append(element);
    $(`#${msg.guid}`).toast("show");

    if (cb) {
      cb();
    }
  })

  /* Triggered live while slider is moved */
  $('#slider').bind('input', function () {
    console.log(`Updating current slider position`);
    log(`Updating current slider position...`);
    $('#sliderPosition').val($('#slider').val());
  });

  /* Triggered when slider is finished moving */
  $('#slider').on('change', function () {
    console.log(`Slider finished moving, updating destination`);
    log(`Slider finished moving, updating destination`);
    $('#desiredPosition').val($('#slider').val());
    sendDesiredPosition($('#slider').val());
  });

  /* Triggered once we have a new destination */
  function sendDesiredPosition(val) {
    console.log(`Sending new desired position`);
    socket.send(val);
  }
  
  /* Reuseable listener for press and hold. On mobile browsers, this action
   * triggers a "contextmenu" event natively which can either be suppressed
   * or handled explicitly with duplicate callback logic
   */
  function longclick(element, callback) {
    var pressTimer;
    element.mouseup(function(){
      clearTimeout(pressTimer);
      return false;
    }).mousedown(function(){
      pressTimer = window.setTimeout(callback, 750);
      return false; 
    });
  }
  // Suppress mobile context menu
  // window.oncontextmenu = function() { return false; }

  /* Save current state as preset */
  longclick($("#presetButtonA"), function() {
    console.log("Updated Preset A")
  });

  longclick($("#presetButtonB"), function() {
    console.log("Updated Preset B")
  });

  /* Apply saved preset state */
  $("#presetButtonA").dblclick(function() {
    console.log("Apply Preset A");
  });

  $("#presetButtonB").dblclick(function() {
    console.log("Apply Preset B");
  });

  /* Fetch and apply latest state from backend */
  $("#sync").on("click", function() {
    console.log("Syncing state")
    location.reload();
  })

  /* Enable toast notifications */
  $(".toast").toast("show");

});

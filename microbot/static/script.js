console.log(`Loaded script.js`);

$(document).ready(function () {
  var socket = io.connect('http://localhost:5000');

  /**
   * Room Enumeration
   */
  // TODO: maybe fetch this from an endpoint?
  const Room = Object.freeze({
    MOTOR: "motor",
    PRESET_ASSIGN: "preset.assign",
    PRESET_APPLY: "preset.apply",
    LOG: "log",
    INFO: "info",
    ERROR: "error",
  });

  /**
   * Rather than logging to the browser console, use a designated
   * DOM element with autoscroll to display granular feedback.
   */
  function log(msg) {
    $('#logs').prepend(`<pre>${msg}</pre>`);
  }

  /* Fetch and apply latest state from backend */
  $("#sync").on("click", function() {
    log("Syncing state")
    location.reload();
  })

  /* Enable toast notifications */
  $(".toast").toast("show");

  socket.on('connect', function () {
    log('Connected to server');
    /* `connect` is a reserved keyword */
    // socket.emit('my_event', {
    //   data: "I'm connected!",
    //   room: 'A'
    // });
  });

  /* Listed for log messages and push to the log component */
  socket.on(Room.LOG, function(msg) {
    log(`[${msg.type}] ${msg.memo}`);
  })

  /* Listen for info messages and push a toast notification */
  socket.on("info", function( msg, cb) {
    console.log(`Received info message: ${JSON.stringify(msg)}`)
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
  /* Suppress mobile context menu */
  // window.oncontextmenu = function() { return false; }

  /* 
   * Triggered once we have a new destination. This is a reusable function
   * which can be recycled for each axis/motor.
   */
  function sendDesiredPosition(motor, value) {
    log(`Sending new desired position for: ${motor}`);
    socket.emit(Room.MOTOR, {
      room: Room.MOTOR,
      data: {
        [motor]: value
      }
    })
  }

  /* Receive the broadcasted motor position state */
  socket.on(Room.MOTOR, function(msg) {
    log(msg.memo);
    // TODO: fix this mess
    // Update current position values
    $('#currentPositionX').val(msg.data.X);
    $('#currentPositionY').val(msg.data.Y);
    $('#currentPositionZ').val(msg.data.Z);
    // Update sliders to match new position
    $("#sliderX").val(msg.data.X);
    $("#sliderY").val(msg.data.Y);
    $("#sliderZ").val(msg.data.Z);
  })

  /**
   * * * * * * * * * * X AXIS * * * * * * * * * * 
   */

  /* Triggered live while slider is moved */
  $('#sliderX').bind('input', function () {
    log(`Updating current X slider position...`);
    $('#sliderPositionX').val($('#sliderX').val());
  });

  /* Triggered when slider is finished moving */
  $('#sliderX').on('change', function () {
    log(`Slider finished moving, updating X destination`);
    $('#desiredPositionX').val($('#sliderX').val());
    sendDesiredPosition("X", $('#sliderX').val());
  });

  /**
   * * * * * * * * * * Y AXIS * * * * * * * * * * 
   */

  /* Triggered live while slider is moved */
  $('#sliderY').bind('input', function () {
    log(`Updating current Y slider position...`);
    $('#sliderPositionY').val($('#sliderY').val());
  });

  /* Triggered when slider is finished moving */
  $('#sliderY').on('change', function () {
    log(`Slider finished moving, updating Y destination`);
    $('#desiredPositionY').val($('#sliderY').val());
    sendDesiredPosition("Y", $('#sliderY').val());
  });

  /**
   * * * * * * * * * * Z AXIS * * * * * * * * * * 
   */

  /* Triggered live while slider is moved */
  $('#sliderZ').bind('input', function () {
    log(`Updating current Z slider position...`);
    $('#sliderPositionZ').val($('#sliderZ').val());
  });

  /* Triggered when slider is finished moving */
  $('#sliderZ').on('change', function () {
    log(`Slider finished moving, updating Z destination`);
    $('#desiredPositionZ').val($('#sliderZ').val());
    sendDesiredPosition("Z", $('#sliderZ').val());
  });

  /**
   * * * * * * * * * * PRESETS * * * * * * * * * * 
   */

  /* Save current state as preset */
  longclick($("#presetButtonA"), function() {
    log("Assigning Preset A");
    socket.emit(Room.PRESET_ASSIGN, {
      room: Room.PRESET_ASSIGN,
      data: "A"
    });
  });

  /* Apply saved preset state */
  $("#presetButtonA").dblclick(function() {
    log("Applying Preset A");
    socket.emit(Room.PRESET_APPLY, {
      room: Room.PRESET_APPLY,
      data: "A"
    });
  });

  /* Save current state as preset */
  longclick($("#presetButtonB"), function() {
    log("Assigning Preset B");
    socket.emit(Room.PRESET_ASSIGN, {
      room: Room.PRESET_ASSIGN,
      data: "B"
    });
  });

  /* Apply saved preset state */
  $("#presetButtonB").dblclick(function() {
    log("Applying Preset B");
    socket.emit(Room.PRESET_APPLY, {
      room: Room.PRESET_APPLY,
      data: "B"
    });
  });

});

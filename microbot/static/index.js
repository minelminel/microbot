console.log(`Loaded index.js`);

$(document).ready(function () {
  var socket = io.connect('http://localhost:5000');

  /**
   * Toggle existing spinner between visible & hidden to provide
   * feedback about long-running processes.
   */
  function isLoading(show) {
    $(`#spinner`).fadeToggle(show);
  }

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
    isLoading(true);
    location.reload();
  })

  /* Enable toast notifications */
  $(".toast").toast("show");

  socket.on('connect', function () {
    log('Connected to server');
    /* `connect` is a reserved keyword */
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
    isLoading(true);
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
    // {[msg.data]: {X: <int>, Y: <int>, Z: <int>}}
    for (const [motor, position] of Object.entries(msg.data)) {
      $(`#currentPosition${motor}`).val(position);
      $(`#sliderPosition${motor}`).val(position);
      $(`#desiredPosition${motor}`).val(position);
      $(`#slider${motor}`).val(position);
    };
    isLoading(false);
  })

  /**
   * * * * * * * * * * AXES * * * * * * * * * * 
   */
  for (const motor of ["X", "Y", "Z"]) {
    /* Triggered live while slider is moved */
    $(`#slider${motor}`).bind('input', function () {
      log(`Updating current ${motor} slider position...`);
      $(`#sliderPosition${motor}`).val($(`#slider${motor}`).val());
    });
  /* Triggered when slider is finished moving */
  $(`#slider${motor}`).on('change', function () {
    log(`Slider finished moving, updating ${motor} destination`);
    $(`#desiredPosition${motor}`).val($(`#slider${motor}`).val());
    sendDesiredPosition(motor, $(`#slider${motor}`).val());
  });
  }

  /**
   * * * * * * * * * * PRESETS * * * * * * * * * * 
   */
  for (const preset of ["A", "B"]) {
    /* Save current state as preset */
    longclick($(`#presetButton${preset}`), function() {
      log(`Assigning Preset ${preset}`);
      socket.emit(Room.PRESET_ASSIGN, {
        room: Room.PRESET_ASSIGN,
        data: preset
      });
    });
    /* Apply saved preset state */
    $(`#presetButton${preset}`).dblclick(function() {
      log(`Applying Preset ${preset}`);
      isLoading(true);
      socket.emit(Room.PRESET_APPLY, {
        room: Room.PRESET_APPLY,
        data: preset
      });
    });
  }

});

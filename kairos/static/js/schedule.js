let dpGlobal = null;

function initScheduleCalendar(today) {
  if (typeof DayPilot === "undefined") {
    console.error("DayPilot not loaded.");
    return;
  }

  const dp = new DayPilot.Calendar("schedule", {
    viewType: "Week",
    startDate: today,
    durationBarVisible: false,
    cellDuration: 30,
    businessBeginsHour: 8,
    businessEndsHour: 22,
    showNonBusiness: false,
    timeRangeSelectedHandling: "JavaScript",
    eventClickHandling: "Disabled",
    eventMoveHandling: "Disabled",
    eventResizeHandling: "Disabled",
    headerLevels: 1,

    onTimeRangeSelected: (args) => {
      toggleSlot(dp, args);
    },
  });

  window.dpCalendar = dp;

  dp.init();
  console.log("dp after init:", dp);
  loadSavedAvailability(dp);
}

function loadSavedAvailability(dp) {
  fetch(window.location.pathname + "availability/load/")
    .then(res => res.json())
    .then((data) => {
      data.blocks.forEach(block => {
        dp.events.add(
          new DayPilot.Event({
            start: block.start,
            end: block.end,
            text: "",
            backColor: block.is_busy ? "#fca5a5" : "#86efac",
            borderColor: block.is_busy ? "#f87171" : "#86efac",
          })
        );
      });
    })
    .catch((err) => console.error("Error loading availability:", err));
}


// Handle slot toggling like When2Meet
function toggleSlot(dp, args) {
  const events = dp.events.list;
  console.log(dp);
  const overlapping = events.filter(
    (e) => e.start <= args.end && e.end >= args.start
  );

  if (overlapping.length) {
    overlapping.forEach(e => dp.events.remove(e));
  } else {
    dp.events.add(
      new DayPilot.Event({
        start: args.start,
        end: args.end,
        text: "",
        backColor: "#86efac",
        borderColor: "#86efac",
      })
    );
  }

  dp.clearSelection();
}

function saveAvailability(dp) {
  if (!dp) {
    console.error("No calendar instance passed to saveAvailability");
    return;
  }
  console.log(dp);
  const blocks = dp.events.map((e) => ({
    start: e.start.toString(),
    end: e.end.toString(),
    date: e.start.toString().split("T")[0],
    is_busy: true,
  }));

  fetch(window.location.pathname + "availability/save/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({ blocks }),
  })
    .then((res) => res.json())
    .then((data) => {
      alert("Availability saved!");
    })
    .catch((err) => console.error("Error saving availability:", err));
}



// CSRF helper
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return null;
}

// // Log or POST selected slots
// function logSelectedSlots(dp) {
//   const selected = dp.events.list.map(e => ({
//     start: e.start.toString(),
//     end: e.end.toString(),
//   }));

//   fetch(window.location.pathname + "availability/save/", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//       "X-CSRFToken": getCookie("csrftoken"),
//     },
//     body: JSON.stringify({ blocks: selected }),
//   });
// }


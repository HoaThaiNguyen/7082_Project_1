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

  dp.init();
}

// Handle slot toggling like When2Meet
function toggleSlot(dp, args) {
  const overlapping = dp.events.list.filter(
    (e) => e.start <= args.end && e.end >= args.start
  );

  if (overlapping.length) {
    overlapping.forEach((e) => dp.events.remove(e));
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
  logSelectedSlots(dp);
}

// Log or POST selected slots
function logSelectedSlots(dp) {
  const selected = dp.events.list.map((e) => ({
    start: e.start.value,
    end: e.end.value,
  }));
  console.log("Selected slots:", selected);

  // Example placeholder for future backend call:
  // fetch("/save_availability/", {
  //   method: "POST",
  //   headers: { "Content-Type": "application/json", "X-CSRFToken": getCSRFToken() },
  //   body: JSON.stringify(selected),
  // });
}
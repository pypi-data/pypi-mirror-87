var timeline = (function ($) {
  "use strict";

  const STATE_TO_LABEL_CLASSNAME = {
    SUCCESS: 'label-success',
    FAILURE: 'label-important',
    PENDING: 'label-default',
    RECEIVED: 'label-default',
    STARTED: 'label-info',
    REVOKED: 'label-warning',
    REJECTED: 'label-warning',
    RETRY: 'label-warning',
    IGNORED: 'label-inverse',
  };

  const receivedStartPicker = $('#receivedStart').datepicker();
  receivedStartPicker.datepicker('setDate', '-2d')
  const receivedEndPicker = $('#receivedEnd').datepicker();
  const timelineContainer = document.getElementById('timeline-graph');
  const workerSelect = $('#worker');
  const taskSelect = $('#task');
  const refreshButton = $('#refreshBtn');

  const timelineChart = TimelinesChart()
    .zScaleLabel('My Scale Units')
    .zQualitative(true)
    .maxLineHeight(16)
    .onSegmentClick(event => {
      event.preventDefault();
      alert(JSON.stringify(event.target.__data__.data.task, null, 4));
    })
    .segmentTooltipContent(segment => {
      const task = segment.data.task;
      return `
        <span class="label ${STATE_TO_LABEL_CLASSNAME[task.state]}">${task.state}</span> ${task.uuid}<br>
        <b>Task</b>: ${task.name} <br>
        <b>Args</b>: ${task.args} <br>
        <b>Kwargs</b>: ${task.kwargs}
        <hr>
        <b>Received</b>: ${toDate(task.received * 1000).toLocaleString()} <br>
        <b>ETA</b>: ${task.eta || '-'} <br>
        <b>Started</b>: ${task.started ? toDate(task.started * 1000).toLocaleString() : '-'} <br>
        <b>Runtime</b>: ${task.runtime || '-'}
      `;
    });
  let timelineChartInitialized = false;

  function groupBy(items, onKey) {
    return items.reduce((result, x) => {
      const key = onKey(x);
      (result[key] = result[key] || []).push(x);
      return result;
    }, {});
  }

  function chop(items, n) {
    let i = 0;
    return items.reduce((result, x) => {
      (result[i] = result[i] || []).push(x);
      i = (i + 1) % n;
      return result;
    }, {});
  }

  function url_prefix() {
    var url_prefix = $('#url_prefix').val();
    if (url_prefix) {
      if (url_prefix.startsWith('/')) {
        return url_prefix;
      } else {
        return '/' + url_prefix;
      }
    }
    return '';
  }

  function toDate(ts) {
    return new Date(ts);
  }

  async function fetchTasks() {
    const params = {};

    const receivedStart = receivedStartPicker.datepicker('getDate');
    const receivedEnd = receivedEndPicker.datepicker('getDate');
    const workerValue = workerSelect.val();
    const taskValue = taskSelect.val();

    if (receivedStart) {
      params['received_start'] = $.datepicker.formatDate("yy-mm-dd 00:00", receivedStart);
    }
    if (receivedEnd) {
      params['received_end'] = $.datepicker.formatDate("yy-mm-dd 00:00", receivedEnd);
    }
    if (workerValue) {
      params['workername'] = workerValue;
    }
    if (taskValue) {
      params['taskname'] = taskValue;
    }

    const response = await fetch(url_prefix() + '/timeline/api/tasks?' + $.param(params));
    if (!response.ok) {
      alert(`Could not retrieve tasks. Request status: ${response.status}`);
      return;
    }

    const responseData = await response.json();
    return responseData.tasks;
  }

  function prepareChartData(tasks) {
    const chartData = [];

    const tasksByWorker = groupBy(tasks, task => task.worker.hostname);
    const workers = Object.keys(tasksByWorker).sort();
    workers.forEach(worker => {
      // sort tasks and chop them into N groups to avoid segment overlapping
      const choppedTasks = chop(
        tasksByWorker[worker].sort((a, b) => a.received - b.received),
        10
      );
      const labels = Object.keys(choppedTasks).sort();

      chartData.push({
        group: worker,
        data: labels.map(label => {
          return {
            label: label.toString().padStart(2, '0'),  // 1 => "01"
            data: choppedTasks[label].map(task => {
              let started = 0;
              let ended;

              if (task.started) {
                started = task.started * 1000;
              } else if (task.eta) {
                started = Date.parse(task.eta);
              } else {
                alert(`Could not generate a segment from a task ${JSON.stringify(task)}`);
              }

              if (task.runtime) {
                ended = started + task.runtime * 1000;
              } else {
                ended = started + 1;
              }

              return {
                timeRange: [toDate(started), toDate(ended)],
                val: task.name,
                task: task
              };
            })
          };
        })
      });
    });

    return chartData;
  }

  function draw() {
    fetchTasks()
      .then(tasks => {
        const data = prepareChartData(tasks);
        timelineChart.data(data);

        if (!timelineChartInitialized) {
          timelineChartInitialized = true;
          timelineChart(timelineContainer);
        }
      });
  }

  refreshButton.click(draw);

  return {
    draw: draw,
  }
}(jQuery));

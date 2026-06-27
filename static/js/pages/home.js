function trackPageView(options = {}) {
    const pageUrl = window.location.pathname + window.location.search;
    const origin = window.location.origin;

    const lastTracked = localStorage.getItem('last-page-view-time');
    const now = Date.now();
    console.log("tracking start");

    // 默认配置
    const config = {
        retryTimes: 3, // 失败重试次数
        interval: 30000, // 上报间隔（默认60秒）
        endpoint: '/api/v1/analyzing/track_page', // 上报接口
        ...options
    };

    if (!lastTracked || now - parseInt(lastTracked) > config.interval) {
        let attempts = 0;

        const sendTrack = () => {
            fetch(`${config.endpoint}?url=${encodeURIComponent(pageUrl)}`, {
              method: 'GET'
          })
            .then(response => {
                if (!response.ok) throw new Error('Server responded with error');
                localStorage.setItem('last-page-view-time', Date.now().toString());
            })
            .catch((e) => {
                console.error(`Track page view attempt ${attempts + 1} failed`, e);
                if (attempts < config.retryTimes) {
                    attempts++;
                    setTimeout(sendTrack, 1000 * attempts);
                }
            });
        };

        sendTrack();
    }
}

function showAlert(message, type) {
    const alertContainer = document.getElementById('liveAlertPlaceholder');
    const alertBox = document.createElement('div');
    alertBox.classList.add('alert', `alert-${type}`, 'alert-dismissible', 'fade', 'show');
    alertBox.setAttribute('role', 'alert');
    alertBox.innerHTML = message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';
    alertContainer.appendChild(alertBox);
    setTimeout(() => {
        if (document.body.contains(alertBox)) {
            var bsAlert = new bootstrap.Alert(alertBox);
            bsAlert.close();
        }
    }, 3000);
}


document.getElementById('messageForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    try {
        const response = await fetch('/api/v1/messaging/messages', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            showAlert("Message submitted successfully!", "success");
            this.reset();
        } else {
            showAlert("Failed to submit message, please check your input.", "danger");
        }
    } catch (error) {
        showAlert("Error: " + error, "danger");
    }
});

document.addEventListener('DOMContentLoaded', () => {
  const chatForm = document.getElementById('chatForm');
  const sendBtn = document.getElementById('sendBtn');
  const questionInput = document.getElementById('floatingTextarea3');
  const answerOutput = document.getElementById('floatingTextarea4');

  chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = questionInput.value.trim();

    if (!message) {
      alert("please input");
      return;
    }

    sendBtn.disabled = true;
    questionInput.disabled = true;
    answerOutput.value = "wait...";

    try {
      const response = await fetch('/api/v1/chatting/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: message,
          model: "gpt-4o-mini"
        })
      });

      const data = await response.json();
      if (data.reply) {
        answerOutput.value = data.reply;
      } else if (data.error) {
        answerOutput.value = "error: " + data.error;
      } else {
        answerOutput.value = "unknown";
      }
    } catch (err) {
      answerOutput.value = "request failure: " + err.message;
    } finally {
      sendBtn.disabled = false;
      questionInput.disabled = false;
      questionInput.focus();
    }
  });
});


document.addEventListener("DOMContentLoaded", function () {
  const ap = new APlayer({
      container: document.getElementById('aplayer'),
      audio: [
          {
              name: 'Autumn\'s Footprints(秋天的脚印)',
              artist: '秋天的脚印',
              url: 'assets/audio/background_music/秋天的脚印/秋天的脚印 - 忘记他 (古典吉他版).mp3',
              cover: 'assets/audio/background_music/秋天的脚印/1.jpg'
          },
          {
            name: 'Listen — It\'s the Sea Wailing.(听是海在悲鸣)',
            artist: '爱需要共鸣',
            url: 'assets/audio/background_music/听是海在悲鸣/7iu、DJ阿沐 - 听是海在悲鸣.mp3',
            cover: 'assets/audio/background_music/听是海在悲鸣/1.jpg'
          }
      ]
  });

  trackPageView();
});

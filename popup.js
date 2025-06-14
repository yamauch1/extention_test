document.getElementById("runPython").addEventListener("click", async () => {
  const outputDiv = document.getElementById("output");
  outputDiv.innerHTML = "実行中...";

  try {
    // Native Hostに接続
    const port = chrome.runtime.connectNative("com.google.chrome.redmine");

    // メッセージ送信
    port.postMessage({ action: "run", parameters: {} });

    // 応答受信
    port.onMessage.addListener((response) => {
      outputDiv.innerHTML = `Pythonからの応答: ${JSON.stringify(response)}`;
    });

    // エラー処理
    port.onDisconnect.addListener(() => {
      if (chrome.runtime.lastError) {
        outputDiv.innerHTML = `エラー: ${chrome.runtime.lastError.message}`;
      }
    });
  } catch (error) {
    outputDiv.innerHTML = `致命的なエラー: ${error.message}`;
  }
});

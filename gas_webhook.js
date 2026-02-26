# gas_webhook.js
function doGet(e) {
  // --- 1. スプレッドシートへの記録処理 ---
  // 先ほどコピーしたスプレッドシートIDをここに貼り付けます
  var sheetId = "YOUR_SPREADSHEET_ID";
  var sheet = SpreadsheetApp.openById(sheetId).getActiveSheet();
  
  // 今の日時を取得して、見やすい形に整える
  var now = new Date();
  var dateStr = Utilities.formatDate(now, "JST", "yyyy/MM/dd");
  var timeStr = Utilities.formatDate(now, "JST", "HH:mm:ss");
  
  // スプレッドシートの最終行にデータを追加する（これだけで記録されます！）
  sheet.appendRow([dateStr, timeStr, "ドアが開きました"]);
  
  
  // --- 2. これまで通りのメール送信処理 ---
  var toAddress = "YOUR_EMAIL_ADDRESS@gmail.com";
  var subject = "【IoTアラート】ドアの開閉を検知しました";
  var body = "玄関のドアが開きました。\n\nログはスプレッドシートに記録されています。";
  
  MailApp.sendEmail(toAddress, subject, body);
  
  
  // ESP32へ成功の返事を返す
  return ContentService.createTextOutput("Logged and Emailed successfully!");
}
function doPost(e) {

  /*
  var url_six = 'XXXXXXXXX   XXXXXXXXX';
  var CHANNEL_ACCESS_TOKEN = 'XXXXXXXXX   XXXXXXXXX';

  var subject = 'XXXXXXXXX   XXXXXXXXX';
  var recipient = 'XXXXXXXXX   XXXXXXXXX';
  var substring = 'XXXXXXXXX   XXXXXXXXX';
  */

  var url_six = 'XXXXXXXXX   XXXXXXXXX';
  var CHANNEL_ACCESS_TOKEN = 'XXXXXXXXX   XXXXXXXXX';

  var subject = 'XXXXXXXXX   XXXXXXXXX';
  var recipient = 'XXXXXXXXX   XXXXXXXXX';
  var substring = 'XXXXXXXXX   XXXXXXXXX';

  var msg = JSON.parse(e.postData.contents);

  //加入判斷，如果包含指定的substring(如自己的userId)，則不用寄信
  if (e.postData.contents.indexOf(substring) == -1) {
    Logger.log(e.postData.contents);
    MailApp.sendEmail(recipient, subject, Logger.getLog());
  }

  // 取出 replayToken 和發送的訊息文字
  var replyToken = msg.events[0].replyToken;
  var userMessage = msg.events[0].message.text;

  if (typeof replyToken === 'undefined') {
    return;
  }

  var payload = {
    "co_id": userMessage
  };

  payload = JSON.stringify(payload);

  var options = {
    'method': 'post',
    "contentType": "application/json",
    'payload': payload
  };

  response_text = '';

  //var response_text = UrlFetchApp.fetch(url_six, options).getContentText();
  var ret = UrlFetchApp.fetch(url_six, options);

  try {
    //把NaN轉為null
    ret = ret.getContentText().replace(/\bNaN\b/g, "null");
    var parsedObj = JSON.parse(ret);
    for (var k in parsedObj) {
      //console.log(k);
      response_text = response_text + k + '\n';
      for (var kd in parsedObj[k]) {
        //null以String()轉為字串
        //console.log(kd.toString() + ': ' + parsedObj[k][kd].toString());      
        response_text = response_text + kd.toString() + ': ' + String(parsedObj[k][kd]) + '\n';

      }
    }
  }

  catch (e) {
    response_text = ret.getContentText() + ' error: ' + e.message + '\n';
  }

  //Logger.log(response_text);
  //MailApp.sendEmail(recipient, subject, Logger.getLog());

  var url = 'https://api.line.me/v2/bot/message/reply';

  UrlFetchApp.fetch(url, {
    'headers': {
      'Content-Type': 'application/json; charset=UTF-8',
      'Authorization': 'Bearer ' + CHANNEL_ACCESS_TOKEN,
    },
    'method': 'post',
    'payload': JSON.stringify({
      'replyToken': replyToken,
      'messages': [{
        'type': 'text',
        'text': response_text
      }],
    }),
  });


}
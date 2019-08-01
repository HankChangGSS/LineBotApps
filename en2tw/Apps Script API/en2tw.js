function doPost(e) {

    /*
        var CHANNEL_ACCESS_TOKEN = 'XXXXXXXXX   XXXXXXXXX';
        var subject = 'XXXXXXXXX   XXXXXXXXX';
        var recipient = 'XXXXXXXXX   XXXXXXXXX';
    */

    var CHANNEL_ACCESS_TOKEN = 'XXXXXXXXX   XXXXXXXXX';
    var subject = 'XXXXXXXXX   XXXXXXXXX';
    var recipient = 'XXXXXXXXX   XXXXXXXXX';

    var s_lng = 'en-US';
    var t_lng = 'zh-TW';

    var bot_reply_eng = '';
    var bot_reply_cht = '';

    var msg = JSON.parse(e.postData.contents);
    Logger.log(msg);
    MailApp.sendEmail(recipient, subject, Logger.getLog());

    var replyToken = msg.events[0].replyToken;
    var userMessage = msg.events[0].message.text;

    if (typeof replyToken === 'undefined') {
        return;
    }

    //https://translate.googleapis.com/translate_a/single?client=gtx&sl=en-US&tl=zh-TW&dt=t&q=Hello
    var url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=' + s_lng + '&tl=' + t_lng + '&dt=t&q=' + userMessage;

    //var ret = '[[["機器學習是人工智能的一個子領域，它使機器能夠在具有經驗的特定任務中得到改進。","Machine Learning is a subfield of Artificial Intelligence that enables machines to improve at a given task with experience.",null,null,3,null,null,null,[[["2876b4f2653853cee22abadb2a855b9a",""]]]],["機器學習是一個非常熱門的話題;","Machine Learning is an extremely hot topic;",null,null,3,null,null,null,[[["2876b4f2653853cee22abadb2a855b9a",""]]]],["在過去的5年中，對經驗豐富的機器學習工程師和數據科學家的需求一直在穩步增長。","the demand for experienced machine learning engineers and data scientists has been steadily growing in the past 5 years.",null,null,3,null,null,null,[[["2876b4f2653853cee22abadb2a855b9a",""]]]],["根據Research and Markets發布的一份報告，到2022年，全球人工智能和機器學習技術部門預計將從14億美元增長到88億美元，預計到2020年人工智能技術部門將創造約230萬個就業崗位。","According to a report released by Research and Markets, the global AI and machine learning technology sectors are expected to grow from $1.4B to $8.8B by 2022 and it is predicted that AI tech sector will create around 2.3 million jobs by 2020.",null,null,3,null,null,null,[[["2876b4f2653853cee22abadb2a855b9a",""]]]]],null,"en"]';
    var ret = UrlFetchApp.fetch(url).getContentText();
    ret = ret.replace(/\bNaN\b/g, "null");
    var parsedObj = JSON.parse(ret);

    if (parsedObj.length > 0) {
        for (var k in parsedObj[0]) {
            if (parsedObj[0][k].length >= 2) {
                bot_reply_eng = bot_reply_eng + String(parsedObj[0][k][1]);
                bot_reply_cht = bot_reply_cht + String(parsedObj[0][k][0]);
            }
        }
    }

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
                'text': bot_reply_eng + '\n' + bot_reply_cht
            }],
        }),
    });

    

}
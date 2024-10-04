import { GoogleGenerativeAI } from "@google/generative-ai";

const predefinedResponses = {
    "送料": "送料は商品と配送先によって異なります。カートに入れた商品を確認し、配送先を入力すると送料が表示されます。",
    "パスワード": "パスワードをお忘れですか？ログイン画面の「パスワードを忘れた方はこちら」からリセットしてください。",
    "返品": "大変申し訳ございませんが、弊社では商品の返品は受け付けておりません。購入前に商品情報をご確認いただき、ご理解の上でご注文いただきますようお願い申し上げます。",
    "支払い": "クレジットカード、デビットカード、銀行振込などがご利用いただけます。",
    "注文状況" : "マイアカウントから注文履歴を確認できます。",
};

// 定型文を返す場合の判定
function checkForKeywords(userInput) {
    // predefinedResponsesの中に含まれる単語をチェック
    for (const keyword in predefinedResponses) {
        if (userInput.includes(keyword)) {
            return predefinedResponses[keyword]; // 対応する定型文を返す
        }
    }
    return null; // 定型文が見つからない場合
}

async function generateResponse(userInput) {

    //APIキーはここおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおお
    const API_KEY = "";
    //うおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおおお


    const genAI = new GoogleGenerativeAI(API_KEY);
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
    console.log("dawdawd");

    try {
        const result = await model.generateContent('あなたはインターネット上で書籍を販売するサイトのFAQアシスタント' + userInput + "対処法を100文字ほどで出力", { max_tokens: 100 });
        document.getElementById('response').innerText = result.response.text();

    } catch (error) {
        console.error("エラーが発生しました:", error);
        document.getElementById('response').innerText = "エラーが発生しました。";
    }
}

document.getElementById('send-btn').addEventListener('click', () => {
    const tb = document.getElementById("response");
    const tbp = document.getElementById("textbox");
    const userInput = document.getElementById('user-input').value;
    tbp.innerText = userInput;
    document.getElementById("textbox").hidden = false;
    document.getElementById("response").hidden = false;
    document.getElementById("hint").hidden = true;

    if (userInput) {
        const predefinedResponse = checkForKeywords(userInput); // 定型文チェック
        if (! (predefinedResponse == null)) {
            console.log(predefinedResponse); 
            tb.innerText = predefinedResponse;
        } else {
            console.log("ボタンが押されました");
            generateResponse(userInput);
            console.log(userInput);
            document.getElementById('user-input').value = '';
        }
    }
});
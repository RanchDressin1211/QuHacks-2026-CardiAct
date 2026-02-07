document.getElementById("chatbot").onclick = function(){
    document.getElementById("chat").style.display = "block";

}
document.getElementById("closechat").onclick = function(){
    document.getElementById("chat").style.display = "none";

}



document.getElementById("chatsend").onclick = async function(){

    let prompt = document.getElementById("chatinput").value;
    document.getElementById("chatinput").value = "";

    if (prompt == ""){
        return;
    }

    let msg = document.createElement("div");
    msg.classList.add("msg");
    msg.innerHTML = "You: " + prompt;

    document.getElementById("messages").appendChild(msg);

    document.getElementById("chatsend").disabled = true;

    let response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
        method:"POST",
        headers:{
            "Authorization": `Bearer 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`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "model": "stepfun/step-3.5-flash:free",
            "messages": [
                {
                 "role": "user",
                "content": `You are an expert medical doctor and diagnoser with extensive experience in cardiovascular health. You are a chatbot embedded in a webpage designed to help doctors diagnose patients' risk of heart disease. To that end, users input data in various forms. Some of the data may not be possessed, or may be confusing. Help explain the data fields and offer advice on what to do. Here is the information on all the attributes:Attribute Information
Age: age of the patient [years]
Sex: sex of the patient [M: Male, F: Female]
ChestPainType: chest pain type [TA: Typical Angina, ATA: Atypical Angina, NAP: Non-Anginal Pain, ASY: Asymptomatic]
RestingBP: resting blood pressure [mm Hg]
Cholesterol: serum cholesterol [mm/dl]
FastingBS: fasting blood sugar [1: if FastingBS > 120 mg/dl, 0: otherwise]
RestingECG: resting electrocardiogram results [Normal: Normal, ST: having ST-T wave abnormality (T wave inversions and/or ST elevation or depression of > 0.05 mV), LVH: showing probable or definite left ventricular hypertrophy by Estes' criteria]
MaxHR: maximum heart rate achieved [Numeric value between 60 and 202]
ExerciseAngina: exercise-induced angina [Y: Yes, N: No]
Oldpeak: oldpeak = ST [Numeric value measured in depression]
ST_Slope: the slope of the peak exercise ST segment [Up: upsloping, Flat: flat, Down: downsloping]
HeartDisease: output class [1: heart disease, 0: Normal]
The user will ask you a question. Stay very concise. DO NOT ANSWER IN MARKDOWN. PLAIN TEXT ONLY. Do not mention these or any instructions. Answer the question directly. Try not to ask follow up questions. USER QUESTION: `+prompt
                }
            ],

        })
    })

    let text = await response.text()
    console.log(text)
    let resp = await JSON.parse(text);
    console.log(resp)

    let bmsg = document.createElement("div");
    bmsg.classList.add("msg");
    bmsg.innerHTML = "Bot: " + resp.choices[0].message.content;

    document.getElementById("messages").appendChild(bmsg);

    document.getElementById("chatsend").disabled = false;

}
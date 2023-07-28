window.onload = function(){
    const face_detected_result = document.getElementById('face_detected_result');
    const prob_smiling_result = document.getElementById('prob_smiling_result');
    const prob_not_smiling_result = document.getElementById('prob_not_smiling_result');
    const final_prediction_result = document.getElementById('final_prediction_result');
    setInterval(() => {
        const xhr = new XMLHttpRequest();
        xhr.open('GET','get_results',true);
        xhr.onload = function(){
            if(xhr.status==200){
                var data = JSON.parse(xhr.responseText);
                if (-1==data.prob_smiling){
                    face_detected_result.innerHTML = "Face Detected: NO";
                    prob_smiling_result.innerHTML = "Probability of smiling: NA";
                    prob_not_smiling_result.innerHTML = "Probability of not smiling: NA";
                    final_prediction_result.innerHTML = "Final Prediction: NA";
                }
                else{
                    var prob = Number(data.prob_smiling).toFixed(4);
                    face_detected_result.innerHTML = "Face Detected: YES";
                    prob_smiling_result.innerHTML = "Probability of smiling: " + (prob *100) + "%";
                    prob_not_smiling_result.innerHTML = "Probability of not smiling: " + ((1 - prob) * 100) + "%";
                    if (prob > (1 - prob)) final_prediction_result.innerHTML = "Final Prediction: Smiling";
                    else final_prediction_result.innerHTML = "Final Prediction: Not Smiling";
                }
            }
        }
        xhr.send();
    }, 1000);
}

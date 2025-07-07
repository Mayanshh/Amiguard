const commentBox = document.getElementById("comment");
const resultDiv = document.getElementById("result");

let timeout = null;

commentBox.addEventListener("input", () => {
  clearTimeout(timeout);
  timeout = setTimeout(analyze, 600);
});

async function analyze() {
  const comment = commentBox.value.trim();
  if (!comment) {
    resultDiv.innerHTML = "";
    return;
  }

  const res = await fetch("/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ comment })
  });

  const data = await res.json();
  const scores = data.attributeScores || {};
  const spans = scores.TOXICITY?.spanAnnotations || [];

  // Highlight toxic parts of the comment
  const highlightedComment = highlightWords(comment, spans);

  let html = `<h3>Live Toxicity Scores:</h3>`;
  for (let key in scores) {
    const value = (scores[key].summaryScore.value * 100).toFixed(2);
    html += `<div class="result-line"><strong>${key}</strong>: ${value}%</div>`;
  }

  html += `
    <div class="highlight-box">
      <h4>Comment Preview:</h4>
      <p>${highlightedComment}</p>
    </div>
  `;

  resultDiv.innerHTML = html;
}

function highlightWords(text, spans) {
  if (!spans || spans.length === 0) return text;

  let result = '';
  let currentIndex = 0;

  spans.sort((a, b) => a.begin - b.begin);

  spans.forEach(span => {
    const toxicPart = text.slice(span.begin, span.end);
    result += text.slice(currentIndex, span.begin);
    result += `<span class="toxic-word">${toxicPart}</span>`;
    currentIndex = span.end;
  });

  result += text.slice(currentIndex);
  return result;
}

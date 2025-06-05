document.addEventListener("DOMContentLoaded", () => {
    const rows = document.querySelectorAll("#bonus-bets-body tr");
    const explainBtn = document.getElementById("explain-btn");

    rows.forEach((row) => {
        row.addEventListener("click", () => {
            // Remove 'selected' from all rows
            rows.forEach((r) => r.classList.remove("selected"));

            // Add 'selected' to clicked row
            row.classList.add("selected");

            // Enable the explain button
            explainBtn.disabled = false;
            explainBtn.classList.add("enabled");
        });
    });


    const modal = document.getElementById("explain-modal");
    const modalBody = document.getElementById("modal-body");
    const closeBtn = document.getElementById("close-modal");

    explainBtn.addEventListener("click", () => {
        const selected = document.querySelector("#bonus-bets-body tr.selected");
        if (selected) {

            modalBody.innerHTML = description(selected);
            modal.classList.remove("hidden");
        }
    });

    closeBtn.addEventListener("click", () => {
        modal.classList.add("hidden");
    });

    window.addEventListener("click", (event) => {
        if (event.target === modal) {
            modal.classList.add("hidden");
        }
    });
});


function description(selected) {

    let spans = selected.getElementsByTagName('span');
    let tds = selected.getElementsByTagName('td');
    let title = tds[0].innerHTML;

    let bonus_amount = document.getElementById("bonus-bet-amount").value;
    let return_rate = document.getElementById("return-rate").value;

    let net_profit = tds[4].innerText.replace("$", "");
    let bonus_name = spans[4].innerText;
    let bonus_odds = spans[3].innerText.split(" ")[1];
    let bonus_maker = spans[3].innerText.split(" ")[0];
    let hedge_amount = spans[6].innerText.split("$")[1]
    let hedge_name = spans[6].innerText.split("$")[0]
    let hedge_odds = spans[5].innerText.split(" ")[1];
    let hedge_maker = spans[5].innerText.split(" ")[0];

    let hedge_payout = ((100 / parseFloat(Math.abs(hedge_odds))) + 1) * parseFloat(hedge_amount);
    let ret = (return_rate / 100) * bonus_amount;
    let hedge_profit = hedge_payout + (return_rate / 100) * bonus_amount;
    hedge_payout = hedge_payout.toFixed(2);
    let bonus_payout = (parseFloat(bonus_odds) / 100 + 1) * parseFloat(bonus_amount);
    bonus_payout = bonus_payout.toFixed(2);
    var template = `

    <h3>${title}</h3>
  <p>
    Since you have a second chance bet, which refunds a loss up to
    <strong>$${bonus_amount}</strong>, you can convert it into 
    <strong>$${net_profit}</strong> by placing <strong>$${bonus_amount}</strong> on 
    <strong>${bonus_name}</strong> at <em>${bonus_maker}</em> for 
    <strong>${bonus_odds}</strong>
    and hedging that bet by placing 
    <strong>$${hedge_amount}</strong> on <strong>${hedge_name}</strong> at 
    <em>${hedge_maker}</em> for <strong>${hedge_odds}</strong>. This assumes that the return rate for a second chance bet
    (site credit, bonus bet, etc.) is about ${return_rate}%.
  </p>

  <p>
    No matter which side wins, you will profit <strong>$${net_profit}</strong>.
  </p>

  <p>
    If the <strong> promotion</strong> side hits, you will make <strong>$${bonus_payout}</strong> (including your stake), 
    but will lose your hedge bet of <strong>$${hedge_amount}</strong>. 
    You will then be left with <strong>$${net_profit}</strong> leftover!<br>
    <b>promotion payout - (hedge stake + promotion stake) = profit </b> <br>
    <b>${bonus_payout} - (${hedge_amount} + ${bonus_amount}) = ${net_profit} </b>
  </p>

  <p>
    If the <strong>hedge</strong> side hits, you will be given back 
    <strong>$${hedge_payout}</strong> (including your stake), and will lose your promotion bet. 
    At this point, you will be at $${(hedge_payout - (parseFloat(hedge_amount) + parseFloat(bonus_amount))).toFixed(2)}. 
    In order to be profitable, you <b> must </b> convert the $${bonus_amount} of bonus or site credit into $${ret}. <br>
    You should make sure that your return rate is really around ${return_rate}% in order to make money!<br>
    If done correctly, you will profit $${net_profit}
    <b> (hedge payout + second chance return) - (hedge stake + promotion stake) = profit </b> <br>
    <b>(${hedge_payout} + ${ret}) - (${hedge_amount} + ${bonus_amount}) = ${net_profit} </b>
  </p>
  
`;


    return template;
}
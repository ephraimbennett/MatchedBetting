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
    let boost_percentage = document.getElementById("boost_percentage").value;

    let net_profit = tds[4].innerText.replace("$", "");
    let bonus_name = spans[4].innerText;
    let bonus_odds = spans[3].innerText.split(" ")[1];
    let bonus_maker = spans[3].innerText.split(" ")[0];
    let hedge_amount = spans[6].innerText.split("$")[1]
    let hedge_name = spans[6].innerText.split("$")[0]
    let hedge_odds = spans[5].innerText.split(" ")[1];
    let hedge_maker = spans[5].innerText.split(" ")[0];

    let hedge_payout = ((100 / parseFloat(Math.abs(hedge_odds))) + 1) * parseFloat(hedge_amount);
    hedge_payout = hedge_payout.toFixed(2);
    let bonus_payout = ((parseFloat(bonus_odds) / 100) * (1 + boost_percentage / 100) + 1) * parseFloat(bonus_amount);
    bonus_payout = bonus_payout.toFixed(2);

    var template = `
    <h3>${title}</h3>
  <p>
    Since you have a <strong>${boost_percentage}%</strong> profit boost for up to
    <strong>$${bonus_amount}</strong>, you can convert it into 
    <strong>$${net_profit}</strong> by placing <strong>$${bonus_amount}</strong> on 
    <strong>${bonus_name}</strong> at <em>${bonus_maker}</em> for 
    <strong>${bonus_odds}</strong> while applying your <strong>${boost_percentage}%</strong> profit boost
    and hedging that bet by placing 
    <strong>$${hedge_amount}</strong> on <strong>${hedge_name}</strong> at 
    <em>${hedge_maker}</em> for <strong>${hedge_odds}</strong>.
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
    <strong>$${hedge_payout}</strong> (including your stake), and will lose your bonus bet. 
    Since the bonus bet is free, your total profit will be <strong>$${net_profit}</strong>!<br>
    <b> hedge payout - (hedge stake + promotion stake) = profit </b> <br>
    <b>${hedge_payout} - (${hedge_amount} + ${bonus_amount}) = ${net_profit} </b>
  </p>
  
`;


    return template;
}
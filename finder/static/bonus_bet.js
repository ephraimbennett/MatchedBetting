document.addEventListener("DOMContentLoaded", () => {
    const rows = document.querySelectorAll("#bonus-bets-body tr");
    const explainBtn = document.getElementById("explain-btn");

    rows.forEach((row, index) => {
        row.addEventListener("click", () => {
            // Remove 'selected' from all rows
            rows.forEach((r) => r.classList.remove("selected"));

            // Add 'selected' to clicked row
            row.classList.add("selected");

            // Enable the explain button
            explainBtn.disabled = false;
            explainBtn.classList.add("enabled");

            row.dataset.index = index;
        });
    });


    const modal = document.getElementById("explain-modal");
    const modalBody = document.getElementById("modal-body");
    const closeBtn = document.getElementById("close-modal");

    const betMap = JSON.parse(document.getElementById('all-bets-data').textContent);

    explainBtn.addEventListener("click", () => {
        const selected = document.querySelector("#bonus-bets-body tr.selected");
        if (selected) {

            modalBody.innerHTML = description(selected, betMap);
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


function description(selected, betMap) {

    let info = betMap[selected.dataset.index];

    let title = info.title;

    let bonus_amount = document.getElementById("bonus-bet-amount").value;

    let net_profit = info.profit.toFixed(2);
    let bonus_name = info.bonus_name;
    let bonus_odds = info.bonus_odds;
    let bonus_maker = info.bonus_bet;
    let hedge_amount = info.hedge_index.toFixed(2);
    let hedge_name = info.hedge_bet;
    
    let hedge_odds = info.hedge_odds;
    let hedge_maker = info.hedge_bet;

    let hedge_payout = ((100 / parseFloat(Math.abs(hedge_odds))) + 1) * parseFloat(hedge_amount);
    hedge_payout = hedge_payout.toFixed(2);
    let bonus_payout = (parseFloat(bonus_odds) / 100) * parseFloat(bonus_amount);

    var template = `
    <h3>${title}</h3>
  <p>
    Since you have a <strong>$${bonus_amount}</strong> bonus bet, you can convert it into 
    <strong>$${net_profit}</strong> by placing your entire bonus bet on 
    <strong>${bonus_name}</strong> at <em>${bonus_maker}</em> for 
    <strong>${bonus_odds}</strong> and hedging that bet by placing 
    <strong>$${hedge_amount}</strong> on <strong>${hedge_name}</strong> at 
    <em>${hedge_maker}</em> for <strong>${hedge_odds}</strong>.
  </p>

  <p>
    No matter which side wins, you will profit <strong>$${net_profit}</strong>.
  </p>

  <p>
    If the <strong>promotion</strong> side hits, you will make <strong>$${bonus_payout}</strong>, 
    but will lose your hedge bet of <strong>$${hedge_amount}</strong>. 
    You will then have <strong>$${net_profit}</strong> leftover!<br>
    <b>promotion payout - hedge stake = profit </b> <br>
    <b>${bonus_payout} - ${hedge_amount} = ${net_profit} </b>
  </p>

  <p>
    If the <strong>hedge</strong> side hits, you will be given back 
    <strong>$${hedge_payout}</strong> (including your stake), and will lose your bonus bet. 
    Since the bonus bet is free, your total profit will be <strong>$${net_profit}</strong>!
    <br>
    <b> hedge payout - hedge stake = profit </b> <br>
    <b>${hedge_payout} - ${hedge_amount} = ${net_profit} </b>
  </p>
`;


    return template;
}
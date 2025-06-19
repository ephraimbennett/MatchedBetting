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

    let return_rate = document.getElementById("return-rate").value;

    let bonus_amount = document.getElementById("bonus-bet-amount").value;

    let net_profit = info.profit.toFixed(2);
    let bonus_name = info.bonus_name;
    let bonus_odds = info.bonus_odds;
    let bonus_maker = info.bonus_bet;
    let hedge_amount = info.hedge_index.toFixed(2);
    let hedge_name = info.hedge_name;
    let hedge_odds = info.hedge_odds;
    let hedge_maker = info.hedge_bet;
    console.log(info);

    bonus_amount = parseFloat(bonus_amount).toFixed(2);
    hedge_amount = parseFloat(hedge_amount).toFixed(2);

    let hedge_payout = ((100 / parseFloat(Math.abs(hedge_odds))) + 1) * parseFloat(hedge_amount);
    hedge_payout = hedge_payout.toFixed(2);
    let ret = (return_rate / 100) * bonus_amount;
    ret = ret.toFixed(2);
    let hedge_profit = hedge_payout + ret;
    //hedge_profit = hedge_profit.toFixed(2);
    
    let bonus_payout = (parseFloat(bonus_odds) / 100 + 1) * parseFloat(bonus_amount);
    bonus_payout = bonus_payout.toFixed(2);

    interim_b = generate_interim(bonus_payout, bonus_amount, hedge_amount);
    interim_h = generate_interim(hedge_payout, bonus_amount, hedge_amount);
    var template = `

    <h3>${title}</h3>
  <p>
    Since you have a qualifying bet, which matches your wager up to 
    <strong>$${bonus_amount}</strong>, you can convert it into 
    <strong>$${net_profit}</strong> by placing <strong>$${bonus_amount}</strong> on 
    <strong>${bonus_name}</strong> at <em>${bonus_maker}</em> for 
    <strong>+${bonus_odds}</strong>
    and hedging that bet by placing 
    <strong>$${hedge_amount}</strong> on <strong>${hedge_name}</strong> at 
    <em>${hedge_maker}</em> for <strong>-${hedge_odds}</strong>. This assumes that the return rate for the credit
    (site credit, bonus bet, etc.) is about ${return_rate}%.
  </p>

  <p>
    No matter which side wins, you will profit <strong>$${net_profit}</strong>.
  </p>

<h3>If the promotional side wins</h3>
<table style="height: auto; width: 100%;">
<tbody>
<tr style="height: 27px;">
<td style="width: 75%; height: 27px;">You will receive your stake of $${bonus_amount} back, and also win $${(bonus_payout - bonus_amount).toFixed(2)} more at +${bonus_odds} odds.</td>
<td style="width: 25%; height: 27px;"><span style="color: #339966;">+ $${(bonus_payout - bonus_amount).toFixed(2)}</span></td>
</tr>
<tr style="height: 13px;">
<td style="width: 75%; height: 13px;">You will lose your hedge stake which was $${hedge_amount}</td>
<td style="width: 25%; height: 13px;"><span style="color: #993300;">- $${hedge_amount}</span></td>
</tr>
<tr style="height: 13.2344px;">
<td style="width: 75%; height: 13.2344px;">At this point you will be ${interim_b.text}</td>
<td style="width: 25%; height: 13.2344px;"><span style="color:${interim_b.color};">$${interim_b.val}</span></td>
</tr>
<tr style="height: 13px;">
<td style="width: 75%; height: 13px;">You use conversion to turn $${bonus_amount} of credit into $${ret}</td>
<td style="width: 25%; height: 13px;"><span style="color: #008000;">+ $${ret}</span></td>
</tr>
<tr style="height: 13px;">
<td style="width: 75%; height: 13px;">You are now up $${net_profit}</td>
<td style="width: 25%; height: 13px;"><span style="color: #008000;">$${net_profit}</span></td>
</tr>
</tbody>
</table>
<h3>&nbsp;If the hedge side wins</h3>
<table style="width: 100%; border-collapse: collapse;">
<tbody>
<tr style="height: 27px;">
<td style="width: 75%; height: 27px;">You will receive your hedge stake of $${hedge_amount} back and also win $${(hedge_payout - hedge_amount).toFixed(2)}</td>
<td style="width: 25%; height: 27px;"><span style="color: #008000;">+$${(hedge_payout - hedge_amount).toFixed(2)}</span></td>
</tr>
<tr style="height: 13px;">
<td style="width: 75%; height: 13px;">You will lose your promotional stake of $${bonus_amount}.</td>
<td style="width: 25%; height: 13px;"><span style="color: #993300;">- $${bonus_amount}</span></td>
</tr>
<tr style="height: 13px;">
<td style="width: 75%; height: 13px;">At this point you will be ${interim_h.text}</td>
<td style="width: 25%; height: 13px;"><span style="color: ${interim_h.color};">&nbsp; $${interim_h.val}</span></td>
</tr>
<tr style="height: 13px;">
<td style="width: 75%; height: 13px;">You use conversion to turn $${bonus_amount} of credit into $${ret}</td>
<td style="width: 25%; height: 13px;"><span style="color: #008000;">+$${ret}</span></td>
</tr>
<tr style="height: 13.4688px;">
<td style="width: 75%; height: 13.4688px;">You are now up $${net_profit}</td>
<td style="width: 25%; height: 13.4688px;"><span style="color: #008000;">&nbsp;$${net_profit}</span></td>
</tr>
</tbody>
</table>
  
`;


    return template;
}


function generate_interim(x, a, b) {
    let interim = "";
    let interim_color = "";
    let interim_val = x - a - b;
    
    interim_val = interim_val.toFixed(2);
    if (interim_val > 0) {
        interim = `up ${interim_val}`;
        interim_color = "#008000";
    } else {
        interim =  `down ${interim_val}`;
        interim_color = "#993300";
    }
    return {
        text: interim,
        color: interim_color,
        val: interim_val
    };
}
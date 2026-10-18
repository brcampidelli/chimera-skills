# Cálculo determinístico

Use valores em centavos ou `Decimal`, nunca `float`, para dinheiro. Este trecho é um **exemplo para o
agente escrever e executar no ambiente do usuário**; ele não faz rede nem envia ordem.

```python
from decimal import Decimal, ROUND_FLOOR

MAX_RISK_PER_TRADE = Decimal("0.02")
MAX_DAILY_LOSS = Decimal("0.05")
MAX_CONSECUTIVE_LOSSES = 3


def check_plan(equity: Decimal, equity_day_open: Decimal, realized_loss_today: Decimal,
               last_results: list[Decimal], side: str, entry: Decimal, stop: Decimal | None,
               value_per_point: Decimal, lot_step: Decimal) -> dict:
    reasons: list[str] = []
    if stop is None:
        return {"approved": False, "max_size": Decimal(0), "reasons": ["regra 3: sem stop loss"]}
    if (side == "long" and stop >= entry) or (side == "short" and stop <= entry):
        return {"approved": False, "max_size": Decimal(0), "reasons": ["regra 3: stop do lado errado"]}

    risk_per_unit = abs(entry - stop) * value_per_point
    budget_trade = equity * MAX_RISK_PER_TRADE
    budget_day = equity_day_open * MAX_DAILY_LOSS - realized_loss_today
    budget = min(budget_trade, budget_day)
    if budget <= 0:
        reasons.append("regra 2: limite diário já consumido")
    max_size = (budget / risk_per_unit / lot_step).to_integral_value(ROUND_FLOOR) * lot_step if budget > 0 else Decimal(0)
    if max_size <= 0 and budget > 0:
        reasons.append("regra 1/2: nem o lote mínimo cabe no risco permitido")

    streak = 0
    for r in reversed(last_results):  # resultados de operações ENCERRADAS, em ordem
        if r < 0:
            streak += 1
        else:
            break
    if streak >= MAX_CONSECUTIVE_LOSSES:
        reasons.append(f"regra 4: {streak} perdas seguidas — parar e revisar")

    return {"approved": not reasons, "max_size": max_size, "risk_per_unit": risk_per_unit,
            "budget_trade": budget_trade, "budget_day": budget_day, "reasons": reasons}
```

## Exemplo conferível

Patrimônio R$ 10.000,00; abertura do dia R$ 10.000,00; perda realizada hoje R$ 200,00; compra a
120,00 com stop em 118,50; R$ 1,00 por ponto por unidade; lote de 1.

- risco por unidade = 1,50 × 1,00 = R$ 1,50
- orçamento por operação = 2% × 10.000 = R$ 200,00
- orçamento do dia = 5% × 10.000 − 200 = R$ 300,00
- orçamento efetivo = R$ 200,00 → tamanho máximo = piso(200 / 1,50) = **133 unidades**
  (risco real = 133 × 1,50 = R$ 199,50)

Escreva um teste com este exemplo antes de usar a função em dado real.

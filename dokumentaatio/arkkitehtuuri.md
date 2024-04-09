# Arkkitehtuurikuvaus

## Luokkakaavio

Alustava luokkakaavio:

```mermaid
classDiagram
    class CalcUI
    class SciCalcView
    class SciCalcController
    class SciCalcDatabase

    CalcUI --|> SciCalcView
    CalcUI --|> SciCalcController
    SciCalcView --|> SciCalcController
    SciCalcController --|> SciCalcDatabase
```

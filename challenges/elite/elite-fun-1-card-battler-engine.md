# Elite Fun Challenge 1: Card Battler Engine

## Quick Pitch

Two players sit down with twenty-card decks. One plays a creature, the other responds with a counterspell, the first answers with an instant that triggers a poison effect, and suddenly nobody at the table can agree on what resolves first or whether the lifesteal creature heals before or after the shield breaks. Card games live or die on rules precision. Build the engine that gets every interaction right, every time, and can replay any disputed match move by move to prove it.

## At a Glance

| | |
|---|---|
| Level | Elite |
| Type | Fun |
| Suggested team size | 3-4 |
| Time box | Full day minimum |
| Recommended scope | Deck validation + effect stack + keyword interactions + deterministic match replay, with deep tests on the rules engine |

## Learning Goals

- Push Copilot agent mode through a genuinely intricate rules domain where correctness depends on precedence and ordering.
- Design a pure, deterministic rules engine and let Copilot generate exhaustive interaction tests against it.
- Encode a rules reference in `docs/` so precisely that an agent can implement a new keyword from documentation alone.
- Practice event-sourced thinking: every match is a seed plus a list of actions, nothing else.
- Learn to review AI-generated logic critically in a domain where subtle bugs are invisible until two effects collide.

## Constraints

- The rules engine must be a pure, separately testable module with no HTTP, UI, or database dependencies.
- Matches must be fully deterministic: identical seed plus identical action list always produces an identical result and event log.
- All randomness (shuffling, coin flips) must flow through a single seeded RNG owned by the engine.
- Effect resolution must use an explicit stack with LIFO resolution; resolution order is never implicit.
- Keyword interactions must follow the documented precedence table; precedence must never be hard-coded per card.
- Match state transitions must be explicit and enforced (`DECK_SELECTION` → `MULLIGAN` → `IN_PROGRESS` → `FINISHED`).
- A finished match is immutable; the only valid operation on it is replay.
- Deck validation rules live in the engine, not in controllers or UI code.

## Non-Goals

- No multiplayer networking or websockets; both players act through the same API or CLI.
- No authentication or user accounts.
- No card artwork, animations, or polished game UI (stretch goals at most).
- No collection management, booster packs, or economy; decks are built from the full card pool.
- No more than the defined keyword set; resist inventing extra mechanics before the core resolves correctly.

## Domain Rules

### Cards

Card fields:

- Name
- Type: `CREATURE`, `SPELL`, `ENCHANTMENT`, `INSTANT`
- Faction: `EMBER`, `TIDE`, `THORN`, `NEUTRAL`
- Energy cost
- Attack and health (creatures only)
- Keywords (zero or more)
- Effect description

Type rules:

- `CREATURE` stays in play, can attack once per turn, dies when health reaches 0.
- `SPELL` resolves once and is discarded; only playable on your own turn.
- `ENCHANTMENT` stays in play and applies a continuous effect.
- `INSTANT` may be played on either player's turn as a response, going on top of the stack.

### Deck Building

- A deck contains exactly 20 cards.
- At most 2 copies of any single card.
- A deck may mix at most 2 factions; `NEUTRAL` cards never count as a faction.
- Deck validation errors must name the exact violated rule.

### Match Lifecycle

A match has:

- Two players
- Status: `DECK_SELECTION`, `MULLIGAN`, `IN_PROGRESS`, `FINISHED`
- RNG seed
- Turn number and active player
- Event log

Rules:

- A match cannot start until both decks pass validation.
- Each player starts at 20 life with 4 cards in hand; the mulligan phase allows one free redraw of the full hand.
- Energy starts at 1 and increases by 1 per turn, capped at 8.
- Drawing from an empty deck deals 1 fatigue damage, increasing by 1 for each subsequent empty draw.
- A player at 0 or less life loses immediately; simultaneous death is a draw.
- A finished match accepts no further actions.

### The Effect Stack

- Playing any card puts its effect on the stack.
- Before the stack resolves, the opposing player gets one chance to respond with an `INSTANT`, which goes on top.
- The stack resolves strictly LIFO: last added, first resolved.
- Triggered abilities ("when X happens, do Y") go on the stack the moment their trigger fires, in active-player-first order when multiple trigger at once.
- Replacement effects ("instead of X, do Y") never use the stack: they modify an event as it happens, applying in the order the effects entered play.

### Keywords

| Keyword | Effect |
|---|---|
| `SHIELD` | The next damage this creature would take is reduced to 0, then the shield breaks. |
| `POISON` | Any damage dealt by this source destroys a creature outright, regardless of health. |
| `HASTE` | The creature may attack on the turn it is played. |
| `LIFESTEAL` | Damage dealt by this source heals its controller for the same amount. |
| `TAUNT` | Enemy creatures must attack a `TAUNT` creature if one exists. |

Interaction precedence, applied in order:

1. Replacement effects (`SHIELD`) modify the damage event first.
2. If any damage still lands, `POISON` applies to the final damage event.
3. `LIFESTEAL` heals based on damage actually dealt after replacements.

Worked examples your engine must get right:

- `POISON` vs `SHIELD`: shield reduces the damage to 0, so poison never applies; the shield breaks.
- `LIFESTEAL` vs `SHIELD`: 0 damage dealt means 0 life gained.
- `LIFESTEAL` + `POISON` attacker: heals for the damage dealt, and the defender dies to poison if any damage landed.

### Combat

- The active player declares one attacker and one target (creature or enemy player) per attack.
- `TAUNT` restricts legal targets before the attack goes on the stack.
- Creatures deal damage to each other simultaneously.
- All combat damage flows through the same damage pipeline as spell damage, so keywords behave identically everywhere.

### AI Opponent

A built-in opponent that plays legally using a greedy heuristic:

- Play the highest-cost affordable card.
- Attack the target that removes the most enemy attack power, else the enemy player.
- Respond with an `INSTANT` only when it prevents lethal damage.

The AI consumes the same engine API as a human player; it never reaches into engine internals.

## Required Endpoints or Flows

```txt
GET    /cards
GET    /cards/{id}

POST   /decks
GET    /decks/{id}
POST   /decks/{id}/validate

POST   /matches
GET    /matches/{id}

POST   /matches/{id}/mulligan
POST   /matches/{id}/play-card
POST   /matches/{id}/respond
POST   /matches/{id}/attack
POST   /matches/{id}/end-turn

GET    /matches/{id}/state
GET    /matches/{id}/log
POST   /matches/{id}/replay
```

A CLI with equivalent commands is an acceptable substitute for HTTP endpoints.

## Architecture Expectations

Keep these concerns separated so they can evolve and be tested independently:

- Card catalog and deck validation
- Match lifecycle and turn structure
- Effect stack and resolution pipeline
- Damage pipeline with keyword precedence
- Event log and replay
- AI opponent
- API or CLI shell

The rules engine must be reachable in tests without spinning up an API, a database, or the AI. The replay feature is the proof: feeding a recorded seed and action list into a fresh engine must reproduce the exact same event log.

## Agent-Ready Deliverables

The repository should contain:

- `docs/domain-model.md`
- `docs/rules-reference.md` (stack, precedence table, worked keyword examples)
- `docs/state-transitions.md`
- `docs/testing.md`
- `.github/copilot-instructions.md`
- `AGENTS.md`

Suggested GitHub issues to seed the board:

1. Create card catalog and deck validation.
2. Implement match lifecycle and turn structure.
3. Implement the effect stack with instant responses.
4. Implement the damage pipeline and keyword precedence.
5. Add combat.
6. Add event log and deterministic replay.
7. Add the greedy AI opponent.
8. Add tests and CI.
9. Add agent-ready documentation.

## Starter Data

Seed a card pool of at least 16 cards covering every type, every faction, and every keyword, plus two prebuilt decks so every team demos against the same baseline.

**Deck "Ember Rush"** (aggressive): cheap `EMBER` creatures with `HASTE`, burn spells, one `SHIELD` enchantment.

**Deck "Tide Control"** (defensive): `TIDE` instants and counters, `TAUNT` and `LIFESTEAL` creatures, card draw.

Sample cards:

| Name | Type | Faction | Cost | Stats / Effect | Keywords |
|---|---|---|---|---|---|
| Cinder Imp | `CREATURE` | `EMBER` | 1 | 2/1 | `HASTE` |
| Tidecaller | `CREATURE` | `TIDE` | 3 | 2/4 | `TAUNT` |
| Thorn Adder | `CREATURE` | `THORN` | 2 | 1/1 | `POISON` |
| Blood Petal | `CREATURE` | `THORN` | 4 | 3/3 | `LIFESTEAL` |
| Fireball | `SPELL` | `EMBER` | 3 | deal 4 damage | |
| Undertow | `INSTANT` | `TIDE` | 2 | counter the top card of the stack | |
| Stone Ward | `ENCHANTMENT` | `NEUTRAL` | 2 | your creatures enter with `SHIELD` | |

**Scripted sample match:** a fixed seed plus a short action script (about 10 actions) ending with an `INSTANT` response resolving on top of the stack. Use it as your demo and as a replay regression test.

## Test Expectations

The suite should prove, at minimum:

- Deck validation rejects wrong size, 3+ copies, and 3-faction decks with named rule violations.
- A match cannot start with an invalid deck, and a finished match rejects all actions.
- The stack resolves LIFO: an `INSTANT` counter resolves before the card it answered.
- `SHIELD` reduces damage to 0 and breaks; `POISON` does not apply through a shield.
- `LIFESTEAL` heals exactly the damage dealt after replacement effects.
- `TAUNT` restricts attack targets.
- Fatigue damage escalates on consecutive empty draws.
- Replay of a recorded seed and action list reproduces an identical event log, byte for byte.

Aim for the damage pipeline and stack resolution to have the deepest coverage, including at least five multi-keyword interaction tests.

## Curveball

Two hours in, the facilitator announces a new keyword: `ECHO`. A card with `ECHO` resolves its effect twice if it was the only card its controller played this turn. The second resolution is a separate stack entry, so the opponent may respond with an `INSTANT` between the two resolutions. Teams must add `ECHO` to the precedence documentation and the engine, prove the double resolution interacts correctly with `SHIELD` and `LIFESTEAL`, and show that all existing replay regression tests still pass unchanged.

## Scoring Rubric

| Criteria | Points | Note |
|---|---|---|
| Domain correctness | 25 | Stack order, keyword precedence, combat, and lifecycle rules behave exactly as specified, including the worked examples. |
| Testing depth | 20 | Damage pipeline, stack, and replay are covered, including multi-keyword interaction cases. |
| Architecture & clarity | 25 | Rules engine is a pure, deterministic module; replay proves it; concerns are separated. |
| Demo quality | 15 | A full match runs end to end with a stack interaction, and a replay reproduces it. |
| Copilot/agent usage story | 15 | Team can show how the rules reference and agent mode drove correct multi-file work. |

## Demo Script

1. **0:00-0:45**: Validate both starter decks, show one deliberately broken deck rejected with a named rule, then start the match and mulligan.
2. **0:45-2:00**: Play through the scripted match: an `INSTANT` response resolving on top of the stack, a `SHIELD` absorbing a `POISON` hit, and a `LIFESTEAL` attack. Narrate the event log as it happens.
3. **2:00-3:00**: Finish the match, then replay it from seed and action list and diff the two event logs live to prove determinism. Close with how Copilot implemented a keyword from the rules reference alone.

## Stretch Ideas

- Add a draft mode where players pick cards alternately from random packs.
- Add a second AI difficulty using one-step lookahead.
- Add a spectator timeline UI that scrubs through the event log.
- Add deck archetype statistics across many AI-vs-AI simulated matches.
- Add a card definition DSL or JSON schema so new cards need no engine changes.
- Add best-of-three matches with sideboarding between games.

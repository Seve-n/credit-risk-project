# User Stories

Each story maps to a requirement in [requirements.md](requirements.md). Not every
requirement gets a fully detailed story yet: US-007 is written at "needs discovery"
maturity, on purpose, mirroring REQ-010's status - a real backlog contains stories at
different levels of readiness, and pretending otherwise would misrepresent how this
analysis actually concluded.

---

### US-001: Real-time document checklist

En tant que **client en cours de demande de crédit**,
je veux **voir immédiatement si un document que je télécharge est manquant ou
invalide**,
afin de **corriger le problème avant de soumettre ma demande plutôt que d'attendre
une revue manuelle pour l'apprendre**.

**Priority:** Must Have
**Dependencies:** None
**Maps to:** REQ-001

**Acceptance criteria:**
- Given I am uploading a document on any channel, When the document is missing a
  required page or field, Then I see a specific message identifying what is missing
  before I can proceed to the next step.
- Given all required documents pass the real-time check, When I submit the
  application, Then `documents_complete` is set to true without requiring a manual
  review trigger for this reason alone.

---

### US-002: Mandatory income and employment fields

En tant qu'**analyste crédit**,
je veux **que le système empêche la soumission d'une demande sans revenu annuel ni
statut d'emploi renseignés**,
afin de **ne plus recevoir de dossiers incomplets sur ces deux champs
spécifiquement**.

**Priority:** Must Have
**Dependencies:** None
**Maps to:** REQ-002

**Acceptance criteria:**
- Given a customer is filling out the application form, When they attempt to submit
  without `annual_income` or `employment_status`, Then the form blocks submission
  and highlights the missing field.
- Given the field is genuinely not applicable (e.g. a customer between jobs), When
  they select an explicit "not currently employed" option, Then the field is
  considered filled, not missing.

---

### US-003: Status visibility during manual review

En tant que **client dont le dossier est en revue manuelle**,
je veux **voir où en est ma demande et un délai estimé**,
afin de **ne pas abandonner ma demande simplement parce que je ne sais pas combien
de temps attendre**.

**Priority:** Must Have
**Dependencies:** None
**Maps to:** REQ-003

**Acceptance criteria:**
- Given my application has entered manual review, When I check my application
  status, Then I see a clear "in review" state and an estimated time range based on
  historical processing time for similar files.
- Given the estimated time range is exceeded, When I check my status again, Then the
  message updates rather than showing a stale estimate.

---

### US-004: Complexity-based triage queue

En tant qu'**analyste crédit**,
je veux **voir les dossiers en attente triés par complexité plutôt que par simple
ordre d'arrivée**,
afin de **traiter en priorité les dossiers simples et consacrer plus de temps aux
dossiers réellement complexes**.

**Priority:** Should Have
**Dependencies:** Requires REQ-001 and REQ-002 in place first, so the complexity
signals used for triage are reliable.
**Maps to:** REQ-004

**Acceptance criteria:**
- Given multiple applications are in the manual review queue, When an analyst opens
  the queue, Then applications are labeled "low complexity" or "full review" based
  on document completeness, previous defaults, and requested amount.
- Given a "low complexity" file, When an analyst opens it, Then the file displays a
  shorter, targeted checklist rather than the full review checklist.

---

### US-005: Pre-screen recommendation for analysts

En tant qu'**analyste crédit**,
je veux **voir une recommandation préliminaire générée automatiquement quand
j'ouvre un dossier en revue manuelle**,
afin de **avoir un point de départ documenté sans que cela remplace mon jugement**.

**Priority:** Should Have
**Dependencies:** REQ-004 (triage).
**Maps to:** REQ-005

**Acceptance criteria:**
- Given an analyst opens a file in manual review, When the file loads, Then a
  pre-screen recommendation (approve-leaning / reject-leaning / needs full review)
  is shown alongside the file, with the factors behind it listed.
- Given the analyst disagrees with the recommendation, When they record a different
  decision, Then the system logs both the recommendation and the analyst's actual
  decision, without blocking the override.

---

### US-006: Default-history flag on the review screen

En tant qu'**analyste crédit**,
je veux **voir immédiatement si le client a un historique de défaut de paiement**,
afin de **ne pas devoir chercher cette information ailleurs pendant la revue**.

**Priority:** Should Have
**Dependencies:** None
**Maps to:** REQ-006

**Acceptance criteria:**
- Given an analyst opens a file with `previous_defaults >= 1`, When the file loads,
  Then a visible flag shows the count and, if available, how long ago the most
  recent default occurred.
- Given `previous_defaults == 0`, When the file loads, Then no flag is shown, to
  avoid diluting the signal with a neutral state.

---

### US-007: Self-service document correction (needs discovery)

En tant que **Product Manager**,
je veux **savoir s'il est possible de laisser un client corriger un document
manquant sans relancer une revue manuelle complète**,
afin de **réduire encore le taux de dossiers incomplets sans complexifier le
processus de vérification**.

**Priority:** Needs discovery, not yet ready for development.
**Dependencies:** Security/Compliance review on re-verification of a corrected
document; IT feasibility assessment on partial re-submission.
**Maps to:** REQ-010

**Acceptance criteria:** *Not yet defined.* Writing acceptance criteria before
Compliance confirms what re-verification a corrected document actually requires
would risk specifying a solution that is not implementable as described.

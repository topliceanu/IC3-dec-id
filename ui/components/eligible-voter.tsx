import { DetailsAccordian } from "./details-accordion"

export function EligibleVoter() {
  return (
    <div>
      <h2 className="text-2xl font-bold">
        Congratulations: you're allowed to vote!
      </h2>
      <p className="text-lg text-muted-foreground">Your details are below.</p>
      <DetailsAccordian />
    </div>
  )
}

import { useAtom } from "jotai"

import { attestationAtom, commitmentAtom, pubkeyAtom } from "@/lib/atoms"
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion"

export function DetailsAccordian() {
  const [commitment, setCommitment] = useAtom(commitmentAtom)
  const [pubkey, setPubkey] = useAtom(pubkeyAtom)
  const [attestation, setAttestation] = useAtom(attestationAtom)

  return (
    <Accordion type="single" collapsible className="w-full">
      <AccordionItem value="item-1">
        <AccordionTrigger>Commitment</AccordionTrigger>
        <AccordionContent>
          {commitment.toLocaleString("fullwide", { useGrouping: false })}
        </AccordionContent>
      </AccordionItem>
      <AccordionItem value="item-2">
        <AccordionTrigger>Public Key</AccordionTrigger>
        <AccordionContent>{pubkey}</AccordionContent>
      </AccordionItem>
      <AccordionItem value="item-3">
        <AccordionTrigger>Attestation</AccordionTrigger>
        <AccordionContent className="overflow-auto">
          <pre>{JSON.stringify(attestation, null, 2)}</pre>
        </AccordionContent>
      </AccordionItem>
    </Accordion>
  )
}

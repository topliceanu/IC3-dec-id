"use client"

import Link from "next/link"
import { zodResolver } from "@hookform/resolvers/zod"
import { useAtom } from "jotai"
import { useForm } from "react-hook-form"
import * as z from "zod"

import {
  attestationAtom,
  commitmentAtom,
  pubkeyAtom,
  zkpAtom,
} from "@/lib/atoms"
import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"

const formSchema = z.object({
  token: z.string(),
})

interface TokenSubmissionFormProps {
  setEligibility: (eligible: boolean) => void
}

export function TokenSubmissionForm({
  setEligibility,
}: TokenSubmissionFormProps) {
  const [commitment, setCommitment] = useAtom(commitmentAtom)
  const [publicKey, setPublicKey] = useAtom(pubkeyAtom)
  const [attestation, setAttestation] = useAtom(attestationAtom)

  // 1. Define your form.
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      token: "",
    },
  })

  // 2. Define a submit handler.
  function onSubmit(values: z.infer<typeof formSchema>) {
    // Do something with the form values.
    // ✅ This will be type-safe and validated.
    console.log(values)

    const postData = async () => {
      const url = DECO_ENDPOINT_URL
      const data = { token: `Bearer ${values.token}` }

      try {
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        })

        const jsonData = await response.json()
        console.log("received from /register route", jsonData)

        setCommitment(jsonData.data.commitment)
        setPublicKey(jsonData.data.public_key)
        setAttestation(jsonData.data.attestation)
        setEligibility(true)
      } catch (error) {
        console.error("Error:", error)
      }
    }
    postData()
    // make call to server to verify user is eligible to vote
    setCommitment("abc")
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          control={form.control}
          name="token"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Submit your token for verification</FormLabel>
              <FormControl>
                <Input placeholder="" {...field} />
              </FormControl>
              <FormDescription>
                Submit your token for validation.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  )
}

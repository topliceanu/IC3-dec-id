"use client"

import Link from "next/link"
import { zodResolver } from "@hookform/resolvers/zod"
import { useAtom } from "jotai"
import { useForm } from "react-hook-form"
import * as z from "zod"

import { commitmentAtom, zkpAtom } from "@/lib/atoms"
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

export function TokenSubmissionForm() {
  const [commitment, setCommitment] = useAtom(commitmentAtom)
  const [zkp, setZkp] = useAtom(zkpAtom)

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
    // make call to server to verify user is eligible to vote
    setCommitment("abc")
    setZkp("def")
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
                Submit your token for verification!
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

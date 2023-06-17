import Link from "next/link"
import { Form } from "react-hook-form"

import { siteConfig } from "@/config/site"
import { buttonVariants } from "@/components/ui/button"
import { CryptoMagicForm } from "@/components/crypto-magic-form"
import { TokenSubmissionForm } from "@/components/token-form"
import { VotingForm } from "@/components/voting-form"

export default function IndexPage() {
  return (
    <section className="container grid items-center gap-6 pb-8 pt-6 md:py-10">
      <div className="flex max-w-[980px] flex-col items-start gap-2">
        <h1 className="text-3xl font-extrabold leading-tight tracking-tighter md:text-4xl">
          dec-ID
        </h1>
        {/* <p className="max-w-[700px] text-lg text-muted-foreground">
          Accessible and customizable components that you can copy and paste
          into your apps. Free. Open Source. And Next.js 13 Ready.
        </p> */}
      </div>
      <div>
        <div className="">
          <h2 className="text-2xl font-bold">Step 1: Token Submission</h2>
          <TokenSubmissionForm />
        </div>
        <div className="mt-8">
          <h2 className="text-2xl font-bold">Step 2: Crypto Magic</h2>
          <CryptoMagicForm />
        </div>
        <div className="mt-8">
          <h2 className="text-2xl font-bold">
            Step 3: Decide where to go for dinner!
          </h2>
          <VotingForm />
        </div>
      </div>
    </section>
  )
}

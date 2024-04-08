'use client'

import { Model } from '@/Model'
import { Form } from '@/components/ui/form'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { zodResolver } from '@hookform/resolvers/zod'
import React from 'react'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { Button } from './ui/button'

const models = Object.values(Model)
const formSchema = z.object({
  model: z.string().min(2, {
    message: 'Name must be at least 2 characters.',
  }),
})

interface EditUsernameFormProps {
  setOpen: React.Dispatch<React.SetStateAction<boolean>>
}

export function SettingsModal({ setOpen }: EditUsernameFormProps) {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      model: models[0],
    },
  })

  function onSubmit(values: z.infer<typeof formSchema>) {
    console.log(values)
    localStorage.setItem('selectedModel', values.model)
    window.dispatchEvent(new Event('storage'))
  }

  const handleChange = (value: string) => {
    form.setValue('model', value)
  }

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className="space-y-4 pt-4"
      >
        <Select onValueChange={handleChange}>
          <SelectTrigger>
            <SelectValue placeholder="Select Model" />
          </SelectTrigger>
          <SelectContent>
            {models.map((model) => {
              return <SelectItem value={model}>{model}</SelectItem>
            })}
          </SelectContent>
        </Select>
        {/* <Select>
          <SelectTrigger>
            <SelectValue placeholder="Architechture" />
          </SelectTrigger>
          <SelectContent>
            {architechture.map((arch) => {
              return <SelectItem value={arch}>{arch}</SelectItem>
            })}
          </SelectContent>
        </Select> */}
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  )
}

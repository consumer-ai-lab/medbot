'use client'

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
import { toast } from 'sonner'
import { z } from 'zod'
import { Button } from './ui/button'

// TODO: Setup models and architechture from here

const models = ['gemini', 'chatgpt']

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
      model: 'gemini',
    },
  })

  function onSubmit(values: z.infer<typeof formSchema>) {
    localStorage.setItem('selectedModel', values.model)
    window.dispatchEvent(new Event('storage'))
    toast.success('Updated successfully')
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault()
    form.setValue('model', e.currentTarget.value)
  }

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className="space-y-4 pt-4"
      >
        {/* <FormField
          control={form.control}
          name=""
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <div className="md:flex gap-4">
                  <Input
                    {...field}
                    type="text"
                    value={name}
                    onChange={(e) => handleChange(e)}
                  />
                  <Button type="submit">Change name</Button>
                </div>
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        /> */}
        <Select>
          <SelectTrigger>
            <SelectValue
              placeholder="Select Model"
              onChange={handleChange}
            />
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

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
import React, { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { Button } from './ui/button'
import { useToast } from './ui/use-toast';
import { getSelectedModel } from '@/lib/model-helper'

const models = Object.values(Model)
const formSchema = z.object({
  model: z.string().min(2, {
    message: 'Name must be at least 2 characters.',
  }),
})


export function SettingsModal() {
  const [selectedModel,setSelectedModel]=useState<string>();

  useEffect(()=>{
    const model=getSelectedModel();
    console.log(model);
    setSelectedModel(model)
  },[])

  const {toast}=useToast();
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
    toast({
      title: "Success",
      description: "Model changed successfully, please close the modal now.",
    })
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
        <Select onValueChange={handleChange} value={selectedModel}>
          <SelectTrigger>
            <SelectValue
              placeholder="Select Model" 
            />
          </SelectTrigger>
          <SelectContent>
            {models.map((model) => {
              return <SelectItem key={model} value={model}>{model}</SelectItem>
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

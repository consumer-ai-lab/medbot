'use client'
import { Form, FormControl, FormField, FormItem, FormLabel } from '@/components/ui/form'
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
import { getSelectedEmbeddingModel, getSelectedModel, getSelectedStrategy } from '@/lib/local-storage-helper'
import { Model } from '@/lib/model-enum'
import { EmbeddingModel } from '@/lib/embedding-model-enum'
import { Strategy } from '@/lib/strategy-enum'

const models = Object.values(Model);
const embeddingModels = Object.values(EmbeddingModel);
const strategies = Object.values(Strategy);
const formSchema = z.object({
  model: z.string().min(2, {
    message: 'Name must be at least 2 characters.',
  }),
  embeddingModel: z.string().min(2, {
    message: 'Name must be at least 2 characters.',
  }),
  strategy: z.string().min(2, {
    message: 'Name must be at least 2 characters.',
  }),
})


export function SettingsModal() {
 
  const { toast } = useToast();
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      model: getSelectedModel() || Model.groq_mistral_8x7b,
      embeddingModel: getSelectedEmbeddingModel() || EmbeddingModel.gemini_pro,
      strategy: getSelectedStrategy() || Strategy.pubmed_search,
    },
  })

  function onSubmit(values: z.infer<typeof formSchema>) {
    console.log(values)
    localStorage.setItem('selectedModel', values.model);
    localStorage.setItem('selectedEmbeddingModel', values.embeddingModel);
    localStorage.setItem('selectedStrategy', values.strategy);
    window.dispatchEvent(new Event('storage'))
    toast({
      title: "Success",
      description: "Model changed successfully, please close the modal now.",
    })
  }

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className="space-y-4 pt-4"
      >
        <FormField
          name="model"
          control={form.control}
          render={({ field }) => {
            return (
              <FormItem>
                <FormLabel>Model</FormLabel>
                <Select
                  onValueChange={field.onChange}
                  value={field.value}
                  defaultValue={field.value}
                >
                  <FormControl>
                    <SelectTrigger>
                      <SelectValue
                        defaultValue={field.value}
                        placeholder="Select Model"
                      />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    {models.map((model) => {
                      return <SelectItem key={model} value={model}>{model}</SelectItem>
                    })}
                  </SelectContent>
                </Select>
              </FormItem>
            )
          }}
        />
        <FormField
          name="embeddingModel"
          control={form.control}
          render={({ field }) => {
            return (
              <FormItem>
                <FormLabel>Embedding Model</FormLabel>
                <Select
                  onValueChange={field.onChange}
                  value={field.value}
                  defaultValue={field.value}
                >
                  <FormControl>
                    <SelectTrigger>
                      <SelectValue
                        defaultValue={field.value}
                        placeholder="Select Embedding Model"
                      />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    {embeddingModels.map((eModel) => {
                      return <SelectItem key={eModel} value={eModel}>{eModel}</SelectItem>
                    })}
                  </SelectContent>
                </Select>
              </FormItem>
            )
          }}
        />
        <FormField
          name="strategy"
          control={form.control}
          render={({ field }) => {
            return (
              <FormItem>
                <FormLabel>Straregy</FormLabel>
                <Select
                  onValueChange={field.onChange}
                  value={field.value}
                  defaultValue={field.value}
                >
                  <FormControl>
                    <SelectTrigger>
                      <SelectValue
                        defaultValue={field.value}
                        placeholder="Select Strategy"
                      />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    {strategies.map((strategy) => {
                      return <SelectItem key={strategy} value={strategy}>{strategy}</SelectItem>
                    })}
                  </SelectContent>
                </Select>
              </FormItem>
            )
          }}
        />
        <Button className='w-full'>Save</Button>
      </form>
    </Form>
  )
}
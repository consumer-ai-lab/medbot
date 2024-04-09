"use client";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { useForm } from "react-hook-form"
import { useToast } from "./ui/use-toast";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
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
import { Button } from "./ui/button";
import { useRouter } from "next/navigation";
import axios from "axios";


const formSchema = z.object({
    email: z.string(),
    user_name:z.string(),
    password: z.string().min(8, {
        message: "Minimum length for password should be 8."
    }).max(20, {
        message: 'Password max be 20 characters big.'
    })
})


export default function RegisterForm() {

    const router = useRouter();
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            email: "",
            password: ""
        }
    })
    const { toast } = useToast();

    const isLoading = form.formState.isLoading;

    async function handleOnSubmit(values: z.infer<typeof formSchema>) {
        try {
            await axios.post(
                '/api/auth/signup',
                values
            )
            toast({
                title: "Welcome",
                description: "Successfully signed up!"
            })
            router.push('/chat');
            router.refresh();
        } catch (error) {
            console.log('[REGISTER_FORM]: ',error);
            toast({
                variant: "destructive",
                description: "Something went wrong, please try again later."
            })
            router.refresh();
        }
    }


    return (
        <Card className="sm:w-[35%] w-[90%]">
            <CardHeader>
                <CardTitle>
                    Signup
                </CardTitle>
                <CardDescription>
                    Sign up to the application
                </CardDescription>
            </CardHeader>
            <CardContent>
                <Form {...form}>
                    <form onSubmit={form.handleSubmit(handleOnSubmit)} className="space-y-8">
                        <FormField
                            control={form.control}
                            name="email"
                            render={({ field }) => {
                                return (
                                    <FormItem>
                                        <FormLabel>Email</FormLabel>
                                        <FormControl>
                                            <Input
                                                placeholder="yash@email.com"
                                                {...field}
                                            />
                                        </FormControl>
                                        <FormDescription>
                                            Please enter a valid email
                                        </FormDescription>
                                        <FormMessage />
                                    </FormItem>
                                )
                            }}
                        />
                        <FormField
                            control={form.control}
                            name="user_name"
                            render={({ field }) => {
                                return (
                                    <FormItem>
                                        <FormLabel>Username</FormLabel>
                                        <FormControl>
                                            <Input
                                                placeholder="yash thombre"
                                                {...field}
                                            />
                                        </FormControl>
                                        <FormDescription>
                                            Your username goes here.
                                        </FormDescription>
                                        <FormMessage />
                                    </FormItem>
                                )
                            }}
                        />
                        <FormField
                            control={form.control}
                            name="password"
                            render={({ field }) => {
                                return (
                                    <FormItem>
                                        <FormLabel>Password</FormLabel>
                                        <FormControl>
                                            <Input
                                                placeholder="linuxrocks@123"
                                                {...field}
                                            />
                                        </FormControl>
                                        <FormDescription>
                                            We suggest you to take a note of your password, as we do have forgot password functionality just yet.
                                        </FormDescription>
                                        <FormMessage />
                                    </FormItem>
                                )
                            }}
                        />
                        <div className="w-full flex justify-center items-center" >
                            <Button className="w-full" disabled={isLoading} size={"lg"} type="submit">Submit</Button>
                        </div>
                    </form>
                </Form>
            </CardContent>
        </Card>
    )
}

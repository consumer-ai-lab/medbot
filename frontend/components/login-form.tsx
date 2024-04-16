"use client";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { useForm } from "react-hook-form";
import { useToast } from "./ui/use-toast";
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Button } from "./ui/button";
import { useRouter } from "next/navigation";
import axios from "axios";
import Link from "next/link";


const formSchema = z.object({
    email: z.string().email({
        message:"Valid email is required."
    }),
    password: z.string().min(8, {
        message: "Minimum length for password should be 8."
    }).max(20, {
        message: "Password max can be 20 characters big."
    })
})


export default function LoginForm() {
    const router = useRouter();
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            email: "",
            password: ""
        }
    })

    const isLoading = form.formState.isLoading;

    const { toast } = useToast();

    async function handleOnSubmit(values: z.infer<typeof formSchema>) {
        try {
            await axios.post(
                '/api/auth/signin',
                values
            )
            toast({
                title: "Welcome",
                description: "Successfully signed in!"
            })
            router.push('/chat');
            router.refresh();
        } catch (error) {
            console.log('[LOGIN_FORM]: ', error);
            // @ts-ignore
            if (error.response.status === 401) {
                toast({
                    variant: "destructive",
                    description: "Invalid Credentials"
                })
            } else {
                toast({
                    variant: "destructive",
                    description: "Something went wrong, please try again later."
                })
            }
            router.refresh();
        }
    }

    return (
        <Card className="sm:w-[35%] w-[90%]">
            <CardHeader>
                <CardTitle>
                    Sign In
                </CardTitle>
                <CardDescription>
                    Sign in to the application
                </CardDescription>
            </CardHeader>
            <CardContent>
                <Form {...form}>
                    <form onSubmit={form.handleSubmit(handleOnSubmit)} className="space-y-8 w-full">
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
                                        <FormMessage/>
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
                                        <FormLabel>
                                            Password
                                        </FormLabel>
                                        <FormControl>
                                            <Input
                                                placeholder="linuxrocks@123"
                                                {...field}
                                            />
                                        </FormControl>
                                        <FormMessage/>
                                    </FormItem>
                                )
                            }}
                        />
                        <div className="w-full flex justify-center items-center">
                            <Button className="w-full" disabled={isLoading} size={"lg"} type="submit">
                                Submit
                            </Button>
                        </div>
                    </form>
                </Form>
            </CardContent>
            <CardFooter className="flex flex-col">
                <CardDescription>
                    Don't have an account?
                </CardDescription>
                <Button
                    variant={"link"}
                    className="font-normal w-full"
                    size={"sm"}
                    asChild
                >
                    <Link href="/auth/sign-up">
                        Sign Up
                    </Link>
                </Button>
            </CardFooter>
        </Card>
    )
}


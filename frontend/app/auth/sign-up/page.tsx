import RegisterForm from "@/components/register-form";


export default function SignUpPage(){
    return (
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[80%] sm:w-[30%] flex justify-center ">
            <RegisterForm/>
        </div>
    )
}
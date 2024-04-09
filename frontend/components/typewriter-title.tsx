"use client";
import Typewriter from "typewriter-effect";

type TypewriterProps = {

}

export default function TypewriterTitle({}:TypewriterProps){
    return (
        <Typewriter
            options={{
                loop:true,
            }}
            onInit={(typewriter)=>{
                typewriter
                .typeString("How to cure common cold?.")
                .pauseFor(1000)
                .deleteAll()
                .typeString("Help me deal with headache.")
                .pauseFor(1000)
                .deleteAll()
                .typeString("I have a fever, what should I do?")
                .pauseFor(1000)
                .deleteAll()
                .start();
            }}
        />
    )
}
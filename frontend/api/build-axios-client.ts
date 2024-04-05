import axios from "axios";
import { headers } from 'next/headers'

export default function buildAxiosClient() {
    if (typeof window === 'undefined') {
        const headersObj = {};
        headers().forEach((header, key) => {
            //@ts-ignore
            headersObj[key] = header;
        });
        return axios.create({
            baseURL: 'http://ingress-nginx-controller.ingress-nginx.svc.cluster.local',
            headers: headersObj
        })
    }else{
        return axios.create({
            baseURL:'/'
        })
    }
}
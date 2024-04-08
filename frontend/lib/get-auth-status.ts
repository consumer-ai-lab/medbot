import buildAxiosClient from "@/api/build-axios-client"

export async function getAuthStatus() {
    try {
      const axiosClient = buildAxiosClient()
      const resp = await axiosClient.get('/api/auth/current-user')
      return resp
    } catch (err) {
      return null
    }
  }
  
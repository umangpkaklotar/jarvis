package com.example.jarvisphone

import android.app.Activity
import android.content.Context
import android.content.Intent
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.net.wifi.WifiManager
import android.os.Bundle
import android.text.format.Formatter
import android.widget.TextView
import fi.iki.elonen.NanoHTTPD
import org.json.JSONObject
import java.io.IOException

class MainActivity : Activity() {

    private lateinit var server: JarvisServer
    private lateinit var statusText: TextView

    // Read securely from BuildConfig (generated via local.properties)
    private val AUTH_TOKEN = BuildConfig.PHONE_TOKEN

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        statusText = TextView(this)
        statusText.textSize = 18f
        statusText.setPadding(32, 32, 32, 32)
        setContentView(statusText)

        val ipAddress = getLocalIpAddress()
        
        statusText.text = "JARVIS Phone\n\n" +
                "Phone IP Address: $ipAddress\n" +
                "Server Port: 8080\n\n" +
                "Server Status: Starting...\n" +
                "Connection Status: Waiting for Jarvis PC"

        server = JarvisServer(this, 8080, AUTH_TOKEN)
        try {
            server.start()
            statusText.text = "JARVIS Phone\n\n" +
                    "Phone IP Address: $ipAddress\n" +
                    "Server Port: 8080\n\n" +
                    "Server Status: Running\n" +
                    "Connection Status: Listening for commands"
        } catch (e: IOException) {
            statusText.text = "JARVIS Phone\n\n" +
                    "Phone IP Address: $ipAddress\n" +
                    "Server Port: 8080\n\n" +
                    "Server Status: Stopped\n" +
                    "Connection Status: Error starting server - ${e.message}"
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        server.stop()
    }

    @Suppress("DEPRECATION")
    private fun getLocalIpAddress(): String {
        val wifiManager = applicationContext.getSystemService(Context.WIFI_SERVICE) as WifiManager
        return Formatter.formatIpAddress(wifiManager.connectionInfo.ipAddress)
    }
}

class JarvisServer(private val context: Context, port: Int, private val token: String) : NanoHTTPD("0.0.0.0", port) {

    // App Allowlist
    private val allowedApps = mapOf(
        "instagram" to "com.instagram.android",
        "whatsapp" to "com.whatsapp",
        "youtube" to "com.google.android.youtube",
        "chrome" to "com.android.chrome",
        "telegram" to "org.telegram.messenger",
        "spotify" to "com.spotify.music",
        "gmail" to "com.google.android.gm",
        "google maps" to "com.google.android.apps.maps",
        "maps" to "com.google.android.apps.maps",
        "camera" to "com.android.camera", // Can vary by manufacturer
        "settings" to "com.android.settings"
    )

    override fun serve(session: IHTTPSession): Response {
        val headers = session.headers
        val authHeader = headers["authorization"] ?: headers["Authorization"]
        
        // 1. Authentication
        if (authHeader != "Bearer $token") {
            return newFixedLengthResponse(Response.Status.UNAUTHORIZED, "application/json", "{\"success\": false, \"message\": \"Unauthorized\"}")
        }

        // 2. Routing
        return when (session.uri) {
            "/status" -> {
                newFixedLengthResponse(Response.Status.OK, "application/json", "{\"success\": true, \"status\": \"ok\", \"service\": \"jarvis_phone\", \"message\": \"JARVIS Phone is connected\"}")
            }
            "/command" -> {
                handleCommand(session)
            }
            else -> {
                newFixedLengthResponse(Response.Status.NOT_FOUND, "application/json", "{\"success\": false, \"message\": \"Not found\"}")
            }
        }
    }

    private fun handleCommand(session: IHTTPSession): Response {
        try {
            val map = HashMap<String, String>()
            session.parseBody(map)
            val postData = map["postData"] ?: return errorResponse("No body")
            
            val json = JSONObject(postData)
            val action = json.optString("action")
            val target = json.optString("target")

            if (action == "open_app") {
                return openApp(target)
            }

            return errorResponse("Unknown action")
        } catch (e: Exception) {
            return errorResponse("Server error: ${e.message}")
        }
    }

    private fun openApp(targetName: String): Response {
        val packageName = allowedApps[targetName.lowercase()]
        if (packageName == null) {
            return errorResponse("$targetName is not supported or not in the allowlist.")
        }

        val launchIntent = context.packageManager.getLaunchIntentForPackage(packageName)
        if (launchIntent != null) {
            launchIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            context.startActivity(launchIntent)
            return successResponse("$targetName opened successfully")
        } else {
            return errorResponse("$targetName is not installed on your phone.")
        }
    }

    private fun successResponse(msg: String): Response {
        return newFixedLengthResponse(Response.Status.OK, "application/json", "{\"success\": true, \"message\": \"$msg\"}")
    }

    private fun errorResponse(msg: String): Response {
        return newFixedLengthResponse(Response.Status.OK, "application/json", "{\"success\": false, \"message\": \"$msg\"}")
    }
}

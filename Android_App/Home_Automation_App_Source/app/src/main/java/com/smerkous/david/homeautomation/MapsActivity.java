package com.smerkous.david.homeautomation;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.FragmentActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.Toast;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.CircleOptions;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.PolylineOptions;

public class MapsActivity extends FragmentActivity implements OnMapReadyCallback {

    private GoogleMap mMap;
    public static double lng = 0;
    public static double lat = 0;

    public static double currentLAT = 0;
    public static double currentLONG = 0;
    public static double currentAlt = 0;

    LocationManager lm;
    LocationListener locationListener;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps);

        lng = MainActivity.lng;
        lat = MainActivity.lat;
        lm = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION)
                != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this,
                Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            return;
        }
        locationListener = new LocationListener() {
            public void onLocationChanged(Location location) {
                mMap.clear();
                currentLONG = location.getLongitude();
                currentLAT = location.getLatitude();
                currentAlt = location.getAltitude();
                LatLng item = new LatLng(lat, lng);
                Log.d("GPS DEVICE LOCATION", String.valueOf(lat) + String.valueOf(lng));
                LatLng current = new LatLng(currentLAT, currentLONG);
                mMap.addMarker(new MarkerOptions().position(item).title("Go here!"));
                mMap.addMarker(new MarkerOptions().alpha(50).position(current).title("You're here!" +
                        "Altitude: "+String.valueOf(currentAlt)));
                //mMap.moveCamera(CameraUpdateFactory.newLatLng(current)); //Uncomment if you want
                                                                             //Camera to move
                drawPath();
            }

            @Override
            public void onStatusChanged(String provider, int status, Bundle extras) {

            }

            @Override
            public void onProviderEnabled(String provider) {

            }

            @Override
            public void onProviderDisabled(String provider) {

            }
        };
        try {
            lm.requestLocationUpdates(LocationManager.GPS_PROVIDER, 350, (float) 0.007, locationListener);
            Location location = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);
            currentLONG = location.getLongitude();
            currentLAT = location.getLatitude();
        }catch(NullPointerException ig)
        {
            Toast.makeText(getApplicationContext(), "ERROR: GPS not found!",
                    Toast.LENGTH_SHORT).show();
            try {
                Location location = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);
                currentLONG = location.getLongitude();
                currentLAT = location.getLatitude();
            }catch (NullPointerException ih)
            {
                Toast.makeText(getApplicationContext(), "ERROR: GPS again not found, turn on GPS!",
                        Toast.LENGTH_SHORT).show();
                currentLONG = 0;
                currentLAT = 0;
            }
        }
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);
    }

    private void drawPath()
    {
        if ( mMap == null)
            return;
        PolylineOptions options = new PolylineOptions();
        options.color(Color.parseColor("#CC0000FF"));
        options.width(4);
        options.visible(true);
        options.add(new LatLng(currentLAT, currentLONG));
        options.add(new LatLng(lat, lng));
        mMap.addPolyline(options);
    }

    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;
        mMap.setIndoorEnabled(true);
        mMap.setMapType(GoogleMap.MAP_TYPE_HYBRID);
        LatLng item = new LatLng(lat, lng);
        LatLng current = new LatLng(currentLAT, currentLONG);
        mMap.addMarker(new MarkerOptions().position(item).title("Go here!"));
        mMap.addMarker(new MarkerOptions().alpha(50).position(current).title("You're here!"));
        mMap.moveCamera(CameraUpdateFactory.zoomTo(19));
        mMap.moveCamera(CameraUpdateFactory.newLatLng(current));
        Toast.makeText(getApplicationContext(), "Start moving then I'll be able to get your " +
                        "location easier, the pin will start moving...",
                Toast.LENGTH_LONG).show();

        drawPath();
    }
}
